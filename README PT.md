# 💳 Credit Card Analyzer – Azure AI & Free OCR / Analisador de Cartões de Crédito – Azure AI & OCR Gratuito

## 🇧🇷 Versão em Português

### 💳 Analisador de Cartões de Crédito – Azure AI & OCR Gratuito

Este aplicativo realiza **análise automatizada de cartões de crédito** para extrair e validar dados como **nome do titular**, **número do cartão**, **data de validade** e **banco emissor**.  
Ele oferece **dois modos de operação**:

- 🔵 **Modo Azure (autenticado)** – usa o serviço **Azure Document Intelligence (prebuilt-credit-card)** para análise de imagem.  
- 🟢 **Modo Gratuito (sem autenticação)** – utiliza **OCR local (Tesseract)** e **regras antifraude** baseadas em regex e validação de Luhn.

---

## 🧱 Estrutura do Projeto

AnalisadorCartoes/  
├─ src/  
│  ├─ app.py ← Interface principal (Streamlit)  
│  ├─ utils/  
│  │   └─ Config.py  
│  ├─ services/  
│  │   ├─ blob_service.py ← Upload (Azure / local)  
│  │   ├─ azure_service.py ← Azure AI prebuilt-credit-card  
│  │   ├─ free_service.py ← OCR local + regex antifraude  
│  │   └─ card_analysis.py ← Orquestra o fluxo e exibe resultado  
│  ├─ __init__.py  
│  
├─ .env ← Configuração local (privado)  
├─ .env.example ← Exemplo público (sem chaves)  
├─ requirements.txt  
├─ Dockerfile  
├─ .gitignore  
└─ README PT.md

---

## 🚀 Modos de Execução

### 🟢 1. Modo Gratuito (sem autenticação Azure)

✅ É o modo **padrão no Docker** — não requer nenhuma modificação nem credenciais.

#### Executando com Docker:
```
docker build -t analisador-cartoes .
docker run -p 8501:8501 analisador-cartoes
```

- O app instala automaticamente o **Tesseract OCR**.  
- Basta acessar no navegador:  
  👉 http://localhost:8501  
- Faça upload de uma **imagem de cartão** (ou insira uma URL pública).

⚠️ **Lembrete:**  
No modo gratuito, lembre-se de instalar o Tesseract OCR no sistema (Windows ou Linux), se estiver rodando fora do Docker.

---

### 🔵 2. Modo Azure (autenticado)

Para usar a análise via **Azure Document Intelligence**:

#### Passos:
1. Faça uma cópia do arquivo de exemplo:
```
cp .env.example .env
```
2. Preencha os campos reais no `.env`:
```
APP_MODE=azure
ENDPOINT=https://SEU-ENDPOINT.cognitiveservices.azure.com/
SUBSCRIPTION_KEY=SUA-CHAVE-DO-AZURE
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=...
CONTAINER_NAME=cartoes
```
3. Execute o container passando as variáveis:
```
docker run -p 8501:8501 --env-file .env analisador-cartoes
```

#### Resultado:
- O app faz upload da imagem no **Azure Blob Storage**.  
- Analisa com o **modelo `prebuilt-credit-card`**.  
- Exibe **nome**, **número**, **validade** e **banco emissor**.

---

### 💻 3. Execução Local (sem Docker)

Para rodar diretamente no seu sistema:
```
pip install -r requirements.txt
streamlit run src/app.py
```

> O modo ativo será determinado pela variável `APP_MODE` no seu `.env`.

---

## ⚙️ Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|-----------|------------|----------|
| `APP_MODE` | Define o modo de operação (`azure` ou `free`) | `free` |
| `ENDPOINT` | Endpoint do Azure Document Intelligence | `https://meuendpoint.cognitiveservices.azure.com/` |
| `SUBSCRIPTION_KEY` | Chave de acesso Azure | `xxxxxx` |
| `AZURE_STORAGE_CONNECTION_STRING` | Connection string do Blob Storage | `DefaultEndpointsProtocol=...` |
| `CONTAINER_NAME` | Nome do container Blob | `cartoes` |
| `FREE_STORAGE_DIR` | Diretório local para modo gratuito | `./storage` |

---

## 🔒 Segurança

- **Nunca publique seu arquivo `.env`** com chaves reais.  
- Use o `.env.example` apenas como modelo.  
- O `.gitignore` já protege o `.env` real de ser versionado.

---

## 🧠 Tecnologias Utilizadas

| Componente | Função |
|-------------|--------|
| **Azure AI Document Intelligence** | Análise inteligente de cartões (`prebuilt-credit-card`) |
| **Azure Blob Storage** | Armazena temporariamente as imagens |
| **Streamlit** | Interface gráfica simples e leve |
| **Tesseract OCR + OpenCV** | Extração de texto local (modo gratuito) |
| **Regex + Luhn** | Heurísticas antifraude no OCR local |

---

## 📦 Dockerfile

O Dockerfile já instala o **Tesseract OCR** e define `APP_MODE=free` por padrão.  
Para usar o modo Azure, basta sobrescrever via `--env-file .env`.

---

## 🧩 Exemplo de Uso

1. Abra o app (http://localhost:8501).  
2. Escolha o modo: **Azure (autenticado)** ou **Gratuito (sem autenticação)**.  
3. Faça upload ou insira a URL de uma imagem de cartão.  
4. Veja o resultado com:
   - Nome do Titular  
   - Número do Cartão (validação Luhn)  
   - Data de Validade  
   - Banco Emissor (se disponível)

---

✅ **Aplicativo pronto para implantação e demonstração.**
