import os
from dotenv import load_dotenv

# Carrega variáveis do .env (se existir)
load_dotenv()

class Config:
    """
    Configuração central do app.
    - APP_MODE: "azure" | "free"
    - Azure: ENDPOINT, SUBSCRIPTION_KEY, AZURE_STORAGE_CONNECTION_STRING, CONTAINER_NAME
    - Free:  FREE_STORAGE_DIR (não usado pelo fluxo atual, mas mantido para compatibilidade)
    """
    APP_MODE = os.getenv("APP_MODE", "azure").strip().lower()

    # 🔵 Azure (autenticado)
    ENDPOINT = os.getenv("ENDPOINT")  # ex: https://<nome>.cognitiveservices.azure.com/
    KEY = os.getenv("SUBSCRIPTION_KEY")
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    CONTAINER_NAME = os.getenv("CONTAINER_NAME")

    # 🟢 Modo gratuito (sem autenticação)
    FREE_STORAGE_DIR = os.getenv("FREE_STORAGE_DIR", "./storage")

    @staticmethod
    def validate_azure():
        """Levanta erro se faltar alguma variável essencial do modo Azure."""
        missing = []
        if not Config.ENDPOINT: missing.append("ENDPOINT")
        if not Config.KEY: missing.append("SUBSCRIPTION_KEY")
        if not Config.AZURE_STORAGE_CONNECTION_STRING: missing.append("AZURE_STORAGE_CONNECTION_STRING")
        if not Config.CONTAINER_NAME: missing.append("CONTAINER_NAME")
        if missing:
            raise RuntimeError(
                "Variáveis ausentes no .env (modo Azure): " + ", ".join(missing)
            )

    @staticmethod
    def is_azure_mode() -> bool:
        return Config.APP_MODE == "azure"

    @staticmethod
    def is_free_mode() -> bool:
        return Config.APP_MODE == "free"
