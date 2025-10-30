from typing import Dict, Any, Optional

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from utils.Config import Config


def analyze_credit_card_url(card_image_url: str) -> Dict[str, Optional[str]]:
    """
    Analisa uma imagem de cartão de crédito a partir da URL (geralmente do Azure Blob)
    usando o modelo prebuilt do Azure Document Intelligence.

    Retorna um dicionário padronizado:
      {
        "card_name": str | None,
        "card_number": str | None,
        "expiry_date": str | None,
        "bank_name": str | None
      }
    """
    if not Config.ENDPOINT or not Config.KEY:
        raise RuntimeError("ENDPOINT e/ou SUBSCRIPTION_KEY ausentes. Configure o .env corretamente.")

    credential = AzureKeyCredential(Config.KEY)
    client = DocumentIntelligenceClient(endpoint=Config.ENDPOINT, credential=credential)

    # Dispara a análise com o modelo prebuilt específico de cartão
    poller = client.begin_analyze_document(
        model_id="prebuilt-credit-card",
        analyze_request=AnalyzeDocumentRequest(url_source=card_image_url)
    )
    result = poller.result()

    # O SDK retorna uma coleção de "documents" com "fields"
    # Extraímos os campos de interesse, tratando ausências com None
    card_name = None
    card_number = None
    expiry_date = None
    bank_name = None

    try:
        for doc in getattr(result, "documents", []) or []:
            fields: Dict[str, Any] = getattr(doc, "fields", {}) or {}
            # Cada campo é um objeto; usamos .get('content') quando disponível
            def get_content(field_name: str) -> Optional[str]:
                f = fields.get(field_name)
                # Alguns SDKs expõem como dict-like; outros como objeto com .content
                if not f:
                    return None
                return getattr(f, "content", None) if hasattr(f, "content") else f.get("content")

            card_name   = card_name   or get_content("CardHolderName")
            card_number = card_number or get_content("CardNumber")
            expiry_date = expiry_date or get_content("ExpirationDate")
            bank_name   = bank_name   or get_content("IssuingBank")

            # se já coletamos tudo, podemos parar
            if card_name or card_number or expiry_date or bank_name:
                break
    except Exception:
        # Mantemos None nos campos se a estrutura vier diferente
        pass

    return {
        "card_name": card_name,
        "card_number": card_number,
        "expiry_date": expiry_date,
        "bank_name": bank_name
    }
