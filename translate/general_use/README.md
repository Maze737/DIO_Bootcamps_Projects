Este documento descreve a solução gratuita de uso geral baseada em modelos Hugging Face, com instruções de instalação, uso e alertas.
This document outlines the free Hugging Face-based solution with setup, usage, and safety notes (English section follows the Portuguese description).

## Descrição (PT-BR)
- Tradução técnica automática sem autenticação usando modelos Helsinki-NLP via `transformers`.
- Entrada suportada: URLs (retorno em Markdown), texto direto (string) e arquivos .docx (gera novo .docx).
- `clean_text` remove ruído básico e há limite de 1,5 MB para downloads e divisão em blocos antes da tradução.

## Requisitos e Instalação (PT-BR)
- Python 3.10+.
- pip install requests beautifulsoup4 python-docx langdetect transformers.
- O primeiro uso baixa o modelo da Hugging Face (necessita conexão). Armazene em cache local para uso offline posterior.

## Uso Rápido (PT-BR)
```python
import sys
sys.path.append("workspace translate")
from general_use.general_use import (
    translate_url_to_markdown,
    translate_text,
    translate_docx,
)

markdown = translate_url_to_markdown("https://exemplo.com/devops", target_lang="pt")
texto = translate_text("Throughput increased after switching the protocol stack.", target_lang="es")
novo_arquivo = translate_docx("caminho/whitepaper.docx", target_lang="en")
```

## Alertas de Segurança (PT-BR)
- Modelos open-source podem não capturar nuances específicas; revise conteúdos críticos.
- A função de URL também impõe HTTP(S) e limite de 1,5 MB, mas ainda pode ser alvo de SSRF se URLs internas forem permitidas.
- O carregamento inicial do modelo pode consumir centenas de MB; garanta espaço e limite de memória.

---

## Description (EN)
- Technical translation without authentication using Helsinki-NLP models through `transformers`.
- Supported input: URLs (Markdown string), plain text, and .docx files (new translated .docx result).
- `clean_text` trims noise, downloads are capped at ~1.5 MB, and text is chunked before translation.

## Requirements & Setup (EN)
- Python 3.10+.
- pip install requests beautifulsoup4 python-docx langdetect transformers.
- First run fetches the model from Hugging Face (requires network); cache it locally for later offline usage.

## Quick Start (EN)
```python
import sys
sys.path.append("workspace translate")
from general_use.general_use import (
    translate_url_to_markdown,
    translate_text,
    translate_docx,
)

markdown = translate_url_to_markdown("https://example.com/cloud", target_lang="pt")
text = translate_text("Firmware rollback restored the cluster availability.", target_lang="fr")
translated_file = translate_docx("path/guide.docx", target_lang="en")
```

## Safety Notes (EN)
- Open models may miss subtle domain nuances; keep human review for sensitive material.
- URL fetching enforces HTTP(S) and a 1.5 MB cap, yet SSRF remains a risk if arbitrary hosts are allowed.
- Model downloads can be large; confirm disk and RAM availability before running in constrained environments.
