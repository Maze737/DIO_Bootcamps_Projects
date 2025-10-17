Este documento explica a solução autenticada com Azure OpenAI, abordando requisitos, uso e alertas de segurança.
This document covers the authenticated Azure OpenAI solution with setup, usage, and safety notes (English section follows the Portuguese description).

## Descrição (PT-BR)
- Tradução técnica automática com Azure OpenAI, preservando terminologia e contexto.
- Entrada suportada: URLs (retorno em Markdown), texto direto (retorno no terminal) e arquivos .docx (gera novo .docx traduzido).
- Higienização de conteúdo com `clean_text`, limitações de tamanho de download e divisão em blocos para evitar estouro de tokens.

## Requisitos e Instalação (PT-BR)
- Python 3.10+.
- pip install requests beautifulsoup4 python-docx langdetect.
- Defina as variáveis de ambiente:
  - `AZURE_OPENAI_ENDPOINT`
  - `AZURE_OPENAI_KEY`
  - `AZURE_OPENAI_DEPLOYMENT`
  - (opcional) `AZURE_OPENAI_API_VERSION`

## Uso Rápido (PT-BR)
```python
import sys
sys.path.append("workspace translate")
from azure_auth.azure_auth import (
    translate_url_to_markdown,
    translate_text,
    translate_docx,
)

markdown = translate_url_to_markdown("https://exemplo.com/artigo", target_lang="pt-BR")
texto = translate_text("Network throughput improved with the new firmware.", target_lang="es")
novo_arquivo = translate_docx("caminho/relatorio.docx", target_lang="pt-BR")
```

## Alertas de Segurança (PT-BR)
- A chave Azure deve ser mantida confidencial; nunca a versione.
- A função `extract_text_from_url` valida esquema e limita downloads a ~2,5 MB, mas ainda pode ser explorada para acessar URLs internas caso executada em redes sensíveis (SSRF). Restrinja URLs se necessário.
- Custos de uso do Azure OpenAI recaem sobre a conta configurada; monitore limites de gasto.

---

## Description (EN)
- Automated technical translation powered by Azure OpenAI, preserving terminology and context.
- Supported input: URLs (Markdown output), plain text (string output), and .docx files (new translated .docx).
- Content sanitation via `clean_text`, guarded download size, and chunking to avoid token limits.

## Requirements & Setup (EN)
- Python 3.10+.
- pip install requests beautifulsoup4 python-docx langdetect.
- Environment variables required:
  - `AZURE_OPENAI_ENDPOINT`
  - `AZURE_OPENAI_KEY`
  - `AZURE_OPENAI_DEPLOYMENT`
  - optional `AZURE_OPENAI_API_VERSION`

## Quick Start (EN)
```python
import sys
sys.path.append("workspace translate")
from azure_auth.azure_auth import (
    translate_url_to_markdown,
    translate_text,
    translate_docx,
)

markdown = translate_url_to_markdown("https://example.com/article", target_lang="pt-BR")
text = translate_text("Latency dropped after enabling jumbo frames.", target_lang="fr")
translated_file = translate_docx("path/report.docx", target_lang="en")
```

## Safety Notes (EN)
- Keep the Azure key secret; never commit it.
- `extract_text_from_url` enforces HTTP(S) and caps downloads (~2.5 MB), yet server-side request forgery remains possible if arbitrary URLs are allowed. Apply additional allowlists where needed.
- Azure OpenAI usage incurs charges on your subscription; watch your quota and costs.
