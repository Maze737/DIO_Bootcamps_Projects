import streamlit as st
from azure.storage.blob import BlobServiceClient, ContentSettings
from utils.Config import Config


def _ensure_container(blob_service_client: BlobServiceClient, container_name: str):
    try:
        container_client = blob_service_client.get_container_client(container_name)
        container_client.create_container()  # cria se não existir
    except Exception:
        # já existe ou não tem permissão para criar — seguimos tentando usar
        pass


def upload_blob(file, file_name: str) -> str | None:
    """
    Sobe o arquivo de imagem para o Azure Blob Storage e retorna a URL pública do blob.
    Este fluxo é usado no modo Azure (alinhado ao exemplo do professor).
    No modo gratuito, o upload ao Blob NÃO é necessário (o processamento é local).
    """
    if not Config.AZURE_STORAGE_CONNECTION_STRING or not Config.CONTAINER_NAME:
        st.error("Faltam configurações do Azure Blob Storage (.env).")
        return None

    try:
        # Conecta no Storage
        blob_service_client = BlobServiceClient.from_connection_string(
            Config.AZURE_STORAGE_CONNECTION_STRING
        )

        # Garante que o container exista
        _ensure_container(blob_service_client, Config.CONTAINER_NAME)

        # Cria o cliente de blob e faz o upload (com content-type)
        blob_client = blob_service_client.get_blob_client(
            container=Config.CONTAINER_NAME,
            blob=file_name
        )

        content_type = getattr(file, "type", None) or "application/octet-stream"
        blob_client.upload_blob(
            file,
            overwrite=True,
            content_settings=ContentSettings(content_type=content_type)
        )

        # Retorna a URL do blob (usada pelo Azure Document Intelligence)
        return blob_client.url

    except Exception as ex:
        st.error(f"Erro ao enviar arquivo para o Azure Blob Storage: {ex}")
        return None
