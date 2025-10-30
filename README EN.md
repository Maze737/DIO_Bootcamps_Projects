# 💳 Credit Card Analyzer – Azure AI & Free OCR / Analisador de Cartões de Crédito – Azure AI & OCR Gratuito


## 🇬🇧 English Version

### 💳 Credit Card Analyzer – Azure AI & Free OCR

This application performs **automated analysis of credit card images**, extracting and validating data such as **cardholder name**, **card number**, **expiration date**, and **issuing bank**.  
It offers **two modes of operation**:

- 🔵 **Azure Mode (authenticated)** – Uses the **Azure Document Intelligence (prebuilt-credit-card)** service for image analysis.  
- 🟢 **Free Mode (unauthenticated)** – Uses **local OCR (Tesseract)** and **antifraud rules** based on regex and Luhn validation.

---

## 🧱 Project Structure

CardAnalyzer/  
├─ src/  
│  ├─ app.py ← Main interface (Streamlit)  
│  ├─ utils/  
│  │   └─ Config.py  
│  ├─ services/  
│  │   ├─ blob_service.py ← Upload (Azure / local)  
│  │   ├─ azure_service.py ← Azure AI prebuilt-credit-card  
│  │   ├─ free_service.py ← Local OCR + antifraud regex  
│  │   └─ card_analysis.py ← Orchestrates the flow and shows results  
│  ├─ __init__.py  
│  
├─ .env ← Local configuration (private)  
├─ .env.example ← Public example (without keys)  
├─ requirements.txt  
├─ Dockerfile  
├─ .gitignore  
└─ README EN.md

---

## 🚀 Execution Modes

### 🟢 1. Free Mode (no Azure authentication)

✅ Default mode in **Docker** — requires no modification or credentials.

#### Run with Docker:
```
docker build -t card-analyzer .
docker run -p 8501:8501 card-analyzer
```

- The app automatically installs **Tesseract OCR**.  
- Access in your browser:  
  👉 http://localhost:8501  
- Upload a **credit card image** or provide a public URL.

⚠️ **Reminder:**  
If you are running outside Docker, install **Tesseract OCR** on your system (Windows or Linux).

---

### 🔵 2. Azure Mode (authenticated)

To use the **Azure Document Intelligence** service:

#### Steps:
1. Copy the example environment file:
```
cp .env.example .env
```
2. Fill in the real values in your `.env`:
```
APP_MODE=azure
ENDPOINT=https://YOUR-ENDPOINT.cognitiveservices.azure.com/
SUBSCRIPTION_KEY=YOUR-AZURE-KEY
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=...
CONTAINER_NAME=cards
```
3. Run the container with your environment variables:
```
docker run -p 8501:8501 --env-file .env card-analyzer
```

#### Result:
- The app uploads the image to **Azure Blob Storage**.  
- Analyzes it using the **`prebuilt-credit-card`** model.  
- Displays **cardholder name**, **card number**, **expiration date**, and **issuing bank**.

---

### 💻 3. Local Execution (no Docker)

To run directly on your system:
```
pip install -r requirements.txt
streamlit run src/app.py
```
> The active mode is determined by `APP_MODE` in your `.env`.

---

## ⚙️ Environment Variables

| Variable | Description | Example |
|-----------|-------------|----------|
| `APP_MODE` | Defines the operation mode (`azure` or `free`) | `free` |
| `ENDPOINT` | Azure Document Intelligence endpoint | `https://myendpoint.cognitiveservices.azure.com/` |
| `SUBSCRIPTION_KEY` | Azure subscription key | `xxxxxx` |
| `AZURE_STORAGE_CONNECTION_STRING` | Azure Blob Storage connection string | `DefaultEndpointsProtocol=...` |
| `CONTAINER_NAME` | Blob container name | `cards` |
| `FREE_STORAGE_DIR` | Local directory for free mode | `./storage` |

---

## 🔒 Security

- **Never publish your `.env` file** with real keys.  
- Use `.env.example` as a safe public template.  
- `.gitignore` already excludes `.env` from being versioned.

---

## 🧠 Technologies Used

| Component | Purpose |
|------------|----------|
| **Azure AI Document Intelligence** | Smart card analysis (`prebuilt-credit-card`) |
| **Azure Blob Storage** | Temporary image storage |
| **Streamlit** | Lightweight web interface |
| **Tesseract OCR + OpenCV** | Local text extraction (Free mode) |
| **Regex + Luhn** | Antifraud validation for OCR results |

---

## 📦 Dockerfile

The Dockerfile installs **Tesseract OCR** and sets `APP_MODE=free` by default.  
To use the Azure mode, override using `--env-file .env`.

---

## 🧩 Example of Use

1. Open the app at [http://localhost:8501](http://localhost:8501).  
2. Choose **Azure (authenticated)** or **Free (unauthenticated)** mode.  
3. Upload or paste a URL for a credit card image.  
4. View results with:
   - Cardholder Name  
   - Card Number (Luhn validated)  
   - Expiration Date  
   - Issuing Bank (if available)

---

## 💡 Quick Notes

- The free mode processes all data **locally**; no external calls are made.  
- The Azure mode ensures **enterprise-grade accuracy and security** using official APIs.  
- Docker builds include Tesseract automatically for convenience.

---