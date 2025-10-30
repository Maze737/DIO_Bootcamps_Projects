"""
Módulo: free_service.py
Modo gratuito (sem autenticação Azure).
Usa OCR local (Tesseract) + heurísticas antifraude simples para extrair:
- Nome do titular
- Número do cartão (validado por Luhn)
- Data de validade (MM/AA ou MM/AAAA)
"""

import io
import re
import hashlib
from typing import Optional, Dict, Any
import requests

try:
    import cv2
    import numpy as np
    import pytesseract
except Exception:
    cv2 = None
    np = None
    pytesseract = None


# =========================
# Utilidades
# =========================

MAX_BYTES = 10 * 1024 * 1024  # 10MB para download via URL


def _sha256(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def _fetch_url_bytes(url: str, timeout: int = 10) -> bytes:
    """Baixa conteúdo da URL de imagem."""
    r = requests.get(url, stream=True, timeout=timeout)
    r.raise_for_status()
    content = b""
    for chunk in r.iter_content(32 * 1024):
        content += chunk
        if len(content) > MAX_BYTES:
            raise ValueError("Arquivo remoto excede 10MB.")
    return content


# =========================
# Heurísticas antifraude
# =========================

CARD_NUMBER_RE = re.compile(r"(?:\d[ -]*?){13,19}")
EXPIRY_RE = re.compile(r"\b(0[1-9]|1[0-2])[\/\- ]?((?:\d{2})|(?:\d{4}))\b")
NAME_LINE_RE = re.compile(r"^[A-Z][A-Z\s\.\-']{2,}$")


def _luhn_ok(number: str) -> bool:
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
    """Executa OCR usando pytesseract."""
    if cv2 is None or np is None or pytesseract is None:
        raise RuntimeError("Dependências OCR não instaladas. Instale Tesseract, OpenCV e numpy.")
    arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Não foi possível decodificar a imagem.")
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(img, lang="por+eng")
    return text


def _extract_fields_from_text(text: str) -> Dict[str, Any]:
    """Extrai número, validade e nome com heurísticas simples."""
    card_number = None
    for m in CARD_NUMBER_RE.finditer(text):
        candidate = m.group().strip()
        if _luhn_ok(candidate):
            card_number = re.sub(r"\D", "", candidate)
            break

    expiry = None
    m = EXPIRY_RE.search(text)
    if m:
        mm, yy = m.group(1), m.group(2)
        if len(yy) == 4:
            yy = yy[-2:]
        expiry = f"{mm}/{yy}"

    card_name = None
    for line in text.splitlines():
        line = line.strip()
        if 3 <= len(line) <= 28 and NAME_LINE_RE.match(line):
            if not CARD_NUMBER_RE.search(line) and not EXPIRY_RE.search(line):
                card_name = line
                break

    return {
        "card_name": card_name,
        "card_number": card_number,
        "expiry_date": expiry,
        "bank_name": None,
        "raw_text": text
    }


# =========================
# Função principal (modo gratuito)
# =========================

def analyze_free(uploaded_file: Optional[io.BytesIO], url_input: Optional[str]) -> Dict[str, Any]:
    """Processa a imagem localmente (upload ou URL)."""
    if uploaded_file is not None:
        data = uploaded_file.read()
        source = f"upload:{uploaded_file.name}"
    elif url_input:
        data = _fetch_url_bytes(url_input)
        source = f"url:{url_input}"
    else:
        raise ValueError("Nenhum arquivo ou URL fornecido.")

    sha = _sha256(data)
    text = _ocr_image_to_text(data)
    fields = _extract_fields_from_text(text)

    return {
        "mode": "free",
        "source": source,
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
