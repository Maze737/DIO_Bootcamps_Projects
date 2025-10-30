import io
import re
import hashlib
from typing import Optional, Dict, Any

import requests
import streamlit as st

from utils.Config import Config
from services.blob_service import upload_blob

# Tente usar nosso serviço Azure unificado.
# Se não existir, caia para o credit_card_service do exemplo do professor.
try:
    from services.azure_service import analyze_credit_card_url as azure_analyze_by_url  # espera URL do blob
except Exception:
    from services.credit_card_service import analyze_credit_card as azure_analyze_by_url  # mesma assinatura

# OCR local e utilidades do modo gratuito
try:
    import cv2
    import numpy as np
    import pytesseract
except Exception:
    cv2 = None
    np = None
    pytesseract = None


# =========================
# Utilidades comuns
# =========================

MAX_BYTES = 10 * 1024 * 1024  # 10MB para URL remota


def _sha256(data: bytes) -> str:
    h = hashlib.sha256(); h.update(data); return h.hexdigest()


def _fetch_url_bytes(url: str, timeout: int = 10) -> bytes:
    """Baixa conteúdo de uma URL (com limites de segurança)."""
    r = requests.get(url, stream=True, timeout=timeout)
    r.raise_for_status()
    content = b""
    for chunk in r.iter_content(32 * 1024):
        content += chunk
        if len(content) > MAX_BYTES:
            raise ValueError("Arquivo remoto excede 10MB")
    return content


# =========================
# Regras/extração MODO GRATUITO
# =========================

CARD_NUMBER_RE = re.compile(r"(?:\d[ -]*?){13,19}")
EXPIRY_RE = re.compile(r"\b(0[1-9]|1[0-2])[\/\- ]?((?:\d{2})|(?:\d{4}))\b")  # MM/AA ou MM/AAAA
NAME_LINE_RE = re.compile(r"^[A-Z][A-Z\s\.\-']{2,}$")  # linha inteira com letras maiúsculas (heurística)

def _luhn_ok(number: str) -> bool:
    """Validação de Luhn para número de cartão."""
    digits = [int(c) for c in re.sub(r"\D", "", number)]
    if len(digits) < 13 or len(digits) > 19:
        return False
    checksum = 0
    parity = (len(digits) - 2) % 2
    for i, d in enumerate(digits):
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0


def _ocr_image_to_text(img_bytes: bytes) -> str:
    if cv2 is None or np is None or pytesseract is None:
        raise RuntimeError("Dependências de OCR não instaladas (opencv-python-headless, numpy, pytesseract).")
    arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Não foi possível decodificar a imagem.")
    # pré-processamento simples
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(img, lang="por+eng")
    return text


def _extract_card_fields_from_text(text: str) -> Dict[str, Any]:
    """
    Heurística simples:
    - número do cartão: primeiro candidato válido no Luhn
    - validade: MM/AA ou MM/AAAA
    - nome: linha em CAIXA ALTA com >= 3 chars (heurística)
    """
    # número
    card_number = None
    for m in CARD_NUMBER_RE.finditer(text):
        candidate = m.group().strip()
        if _luhn_ok(candidate):
            card_number = re.sub(r"\D", "", candidate)
            break

    # validade
    expiry = None
    m = EXPIRY_RE.search(text)
    if m:
        mm, yy = m.group(1), m.group(2)
        if len(yy) == 4:
            yy = yy[-2:]  # normaliza para AA
        expiry = f"{mm}/{yy}"

    # nome (procura linha com padrão de nome em maiúsculas)
    card_name = None
    for line in text.splitlines():
        line = line.strip()
        if 3 <= len(line) <= 28 and NAME_LINE_RE.match(line):
            # evita capturar linhas que são número/expiração
            if not CARD_NUMBER_RE.search(line) and not EXPIRY_RE.search(line):
                card_name = line
                break

    return {
        "card_name": card_name,
        "card_number": card_number,
        "expiry_date": expiry,
        # No modo gratuito não inferimos banco emissor com confiança
        "bank_name": None,
        "raw_text": text
    }


def _analyze_free(uploaded_file: Optional[io.BytesIO], url_input: Optional[str]) -> Dict[str, Any]:
    """Processa no modo gratuito: OCR local + heurísticas."""
    if uploaded_file is not None:
        data = uploaded_file.read()
        filename = uploaded_file.name
        src = f"upload:{filename}"
    elif url_input:
        data = _fetch_url_bytes(url_input)
        src = f"url:{url_input}"
    else:
        raise ValueError("Forneça arquivo ou URL no modo gratuito.")

    sha = _sha256(data)
    text = _ocr_image_to_text(data)
    fields = _extract_card_fields_from_text(text)

    return {
        "mode": "free",
        "source": src,
        "hash_sha256": sha,
        "extraction": {
            "CardHolderName": fields.get("card_name"),
            "CardNumber": fields.get("card_number"),
            "ExpirationDate": fields.get("expiry_date"),
            "IssuingBank": fields.get("bank_name"),
        },
        "debug": {
            "text": fields.get("raw_text"),
        }
    }


# =========================
# Fluxo principal usado pelo app
# =========================

def analyze_card_and_show(mode: str, uploaded: Optional[io.BytesIO], url_input: Optional[str]) -> None:
    """
    Orquestra o fluxo e exibe o resultado no Streamlit.

    mode:
      - "azure" -> upload para Blob e análise por URL no modelo prebuilt-credit-card
      - "free"  -> OCR local + regex (upload OU URL)
    """
    if mode == "azure":
        if uploaded is None:
            st.error("No modo Azure, é necessário enviar um arquivo de imagem.")
            return

        st.info("➡️ Enviando arquivo para o Azure Blob Storage…")
        blob_url = upload_blob(uploaded, uploaded.name)
        if not blob_url:
            st.error("Falha no upload ao Blob Storage.")
            return

        st.success("Upload concluído.")
        st.write("**URL do Blob:**")
        st.code(blob_url, language="text")

        st.info("🔎 Analisando com Azure Document Intelligence (prebuilt-credit-card)…")
        try:
            # A função espera uma URL pública do blob
            result = azure_analyze_by_url(blob_url)
        except Exception as e:
            st.error(f"Erro ao chamar o Azure Document Intelligence: {e}")
            return

        # Normaliza resultado em um dicionário padrão de exibição
        normalized = _normalize_azure_result(result)
        _show_result(normalized)

    else:
        # MODO GRATUITO
        st.info("🔎 Processando localmente (OCR + heurísticas)…")
        try:
            result = _analyze_free(uploaded_file=uploaded, url_input=url_input)
        except Exception as e:
            st.error(f"Erro no modo gratuito: {e}")
            return
        _show_result(result)


def _normalize_azure_result(azure_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Aceita tanto o retorno do azure_service.analyze_credit_card_url()
    quanto do credit_card_service.analyze_credit_card() (exemplo do professor).
    Normaliza para o mesmo formato do modo 'free'.
    """
    # Se o payload já vier como um dicionário com as chaves esperadas:
    # (Ex.: professor retorna dict simples com card_name, card_number, expiry_date, bank_name)
    if all(k in azure_payload for k in ("card_name", "card_number", "expiry_date", "bank_name")):
        return {
            "mode": "azure",
            "source": "azure-blob",
            "hash_sha256": None,  # no fluxo Azure o hash é opcional
            "extraction": {
                "CardHolderName": azure_payload.get("card_name"),
                "CardNumber": azure_payload.get("card_number"),
                "ExpirationDate": azure_payload.get("expiry_date"),
                "IssuingBank": azure_payload.get("bank_name"),
            }
        }

    # Caso venha como objeto completo do SDK convertido para dict,
    # você pode mapear aqui conforme a estrutura retornada.
    return {
        "mode": "azure",
        "source": "azure-blob",
        "hash_sha256": None,
        "extraction": {
            "CardHolderName": azure_payload.get("CardHolderName") or azure_payload.get("card_name"),
            "CardNumber": azure_payload.get("CardNumber") or azure_payload.get("card_number"),
            "ExpirationDate": azure_payload.get("ExpirationDate") or azure_payload.get("expiry_date"),
            "IssuingBank": azure_payload.get("IssuingBank") or azure_payload.get("bank_name"),
        }
    }


def _show_result(payload: Dict[str, Any]) -> None:
    """Renderiza o resultado no Streamlit de forma amigável."""
    st.subheader("Resultado da Análise")

    meta_cols = st.columns(3)
    meta_cols[0].metric("Modo", payload.get("mode", "").upper())
    meta_cols[1].metric("Fonte", payload.get("source", "-"))
    meta_cols[2].metric("Hash SHA256", (payload.get("hash_sha256") or "-")[:16] + "…")

    extraction = payload.get("extraction", {}) or {}
    st.write("**Campos extraídos:**")
    st.json({
        "CardHolderName": extraction.get("CardHolderName"),
        "CardNumber": extraction.get("CardNumber"),
        "ExpirationDate": extraction.get("ExpirationDate"),
        "IssuingBank": extraction.get("IssuingBank"),
    })

    if payload.get("mode") == "free":
        with st.expander("Texto completo (OCR)", expanded=False):
            debug = payload.get("debug", {}) or {}
            st.text_area("texto", debug.get("text", ""), height=240)
