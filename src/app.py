import streamlit as st
from utils.Config import Config
from services.card_analysis import analyze_card_and_show

st.set_page_config(page_title="Analisador de Cartões • Azure / Gratuito", layout="centered")
st.title("Analisador de Cartões de Crédito")
st.caption("Escolha o modo de operação e envie uma imagem do cartão (POC de demonstração).")

# seleção de modo (padrão vindo do .env, mas o usuário pode trocar na UI)
default_mode = "Azure (autenticado)" if Config.APP_MODE == "azure" else "Gratuito (sem autenticação)"
mode = st.radio("Modo de operação:", ["Azure (autenticado)", "Gratuito (sem autenticação)"], index=0 if default_mode.startswith("Azure") else 1)

st.divider()

# UPLOAD / URL
col1, col2 = st.columns(2)
with col1:
    uploaded = st.file_uploader("Envie uma imagem (PNG/JPG/JPEG)", type=["png", "jpg", "jpeg"])

with col2:
    url_input = st.text_input("Ou informe uma URL de imagem (usado no modo gratuito)", placeholder="https://exemplo.com/cartao.jpg")

# Botão de ação
if st.button("Analisar", use_container_width=True, disabled=(uploaded is None and not url_input)):
    # Roteamento por modo
    if mode.startswith("Azure"):
        # 🔵 AZURE: segue o fluxo do professor (upload -> blob -> analisar com prebuilt-credit-card)
        if not uploaded:
            st.error("No modo Azure, envie um arquivo de imagem do cartão.")
        else:
            analyze_card_and_show(mode="azure", uploaded=uploaded, url_input=None)
    else:
        # 🟢 GRATUITO: OCR local + regex (aceita upload OU URL)
        if not uploaded and not url_input:
            st.error("No modo Gratuito, envie um arquivo ou informe uma URL.")
        else:
            analyze_card_and_show(mode="free", uploaded=uploaded, url_input=url_input or None)

st.info("Este app é uma POC. Não use dados sensíveis de cartões reais.")
