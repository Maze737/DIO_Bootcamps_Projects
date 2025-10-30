📘 README — DIO_Bootcamps_Projects

🇧🇷 **Descrição (Português)**  
> **Nota:** A versão em inglês está logo abaixo desta seção.  

# 🧭 DIO Bootcamps Projects  
Repositório central contendo todos os projetos desenvolvidos durante os bootcamps da **Digital Innovation One (DIO)**.  
Cada projeto está organizado em sua **própria branch**, permitindo que sejam executados e estudados separadamente, mantendo um histórico limpo e independente.

## 📂 Estrutura do Repositório  
DIO_Bootcamps_Projects/
├── main/                      → Índice geral e documentação
├── workspace_fraude/          → Projeto: Analisador de Fraudes com Azure AI
└── workspace_translate/       → Projeto: Tradutor Automático (Azure Challenge)

## 🌿 Estrutura de Branches  
| Branch | Descrição | Linguagem Principal |
|---------|------------|--------------------|
| **main** | Contém este README e o índice dos projetos. | Markdown |
| **workspace_fraude** | Projeto de análise antifraude de documentos e cartões, com Azure AI e modo gratuito via OCR. | Python |
| **workspace_translate** | Projeto de tradução automática de textos, com Azure Translator API e opção gratuita via API pública. | Python |

## 🚀 Como Navegar  
1. Clique na lista suspensa de branches (canto superior esquerdo no GitHub).  
2. Selecione a branch desejada (`workspace_fraude` ou `workspace_translate`).  
3. Leia o `README.md` do projeto para instruções detalhadas de instalação e execução.

🔗 **Acesso rápido**  
- [Analisador de Fraudes (workspace_fraude)](https://github.com/Maze737/DIO_Bootcamps_Projects/tree/workspace_fraude)  
- [Tradutor Automático (workspace_translate)](https://github.com/Maze737/DIO_Bootcamps_Projects/tree/workspace_translate)  

## 🧩 Objetivo dos Projetos  
- **workspace_fraude** → Desenvolver um sistema de **análise automatizada de documentos** usando **Azure Document Intelligence** para detectar fraudes, validar autenticidade e aumentar a segurança de processos.  
  - Inclui modo **Azure autenticado** e **modo gratuito** (com OCR local).  

- **workspace_translate** → Criar uma aplicação de **tradução de textos multilíngue** com **Azure Translator API**, incluindo fallback gratuito com **Deep Translator** para usuários sem credenciais Azure.  

## ⚙️ Tecnologias Utilizadas  
- Python 3.11+  
- Streamlit (interface web)  
- Azure Cognitive Services  
- Azure Storage Blob  
- Tesseract OCR *(para o modo gratuito do app fraude)*  
- Docker *(opcional para execução isolada)*  

## 🧠 Sobre  
Este repositório serve como um **portfólio prático** dos projetos desenvolvidos durante o aprendizado em Cloud e IA no ecossistema DIO.  
Cada aplicação demonstra o uso de **boas práticas**, **segurança em credenciais (.env + .gitignore)** e **documentação bilíngue** para facilitar o uso global.

## 🧾 Licença  
Este projeto é distribuído sob a licença **MIT**, permitindo uso, modificação e distribuição livremente, desde que os créditos sejam mantidos.

──────────────────────────────────────────────────────────────

🇬🇧 **Description (English)**  
> **Note:** This English version mirrors the Portuguese content above.  

# 🧭 DIO Bootcamps Projects  
Central repository containing all projects developed during the **Digital Innovation One (DIO)** bootcamps.  
Each project is stored in its **own branch**, allowing isolated testing, independent versioning, and clear documentation.

## 📂 Repository Structure  
DIO_Bootcamps_Projects/
├── main/                      → General index and documentation
├── workspace_fraude/          → Project: Fraud Analyzer with Azure AI
└── workspace_translate/       → Project: Automatic Translator (Azure Challenge)

## 🌿 Branch Overview  
| Branch | Description | Main Language |
|---------|--------------|----------------|
| **main** | Contains this README and project index. | Markdown |
| **workspace_fraude** | Automated fraud analysis for documents and credit cards using Azure AI and a local OCR fallback mode. | Python |
| **workspace_translate** | Automatic text translation using Azure Translator API and free public API fallback. | Python |

## 🚀 How to Navigate  
1. Open the branch dropdown menu on GitHub (top-left).  
2. Select the desired branch (`workspace_fraude` or `workspace_translate`).  
3. Open that branch’s `README.md` for full setup and usage instructions.

🔗 **Quick Access**  
- [Fraud Analyzer (workspace_fraude)](https://github.com/Maze737/DIO_Bootcamps_Projects/tree/workspace_fraude)  
- [Automatic Translator (workspace_translate)](https://github.com/Maze737/DIO_Bootcamps_Projects/tree/workspace_translate)  

## 🧩 Project Purposes  
- **workspace_fraude** → Builds an **automated document verification system** using **Azure Document Intelligence** to detect fraud, validate authenticity, and enhance security for business workflows.  
  - Includes **Azure-authenticated mode** and **free OCR mode** for non-Azure users.  

- **workspace_translate** → Provides a **multilingual text translation application** powered by **Azure Translator API**, with a **free public API fallback** (Deep Translator).  

## ⚙️ Technologies  
- Python 3.11+  
- Streamlit (web interface)  
- Azure Cognitive Services  
- Azure Storage Blob  
- Tesseract OCR *(for the free mode of the fraud analyzer)*  
- Docker *(optional for containerized execution)*  

## 🧠 About  
This repository serves as a **hands-on portfolio** for all DIO bootcamp projects focused on Cloud Computing and Artificial Intelligence.  
Each branch follows **secure credential management (.env + .gitignore)** and **bilingual documentation** for global accessibility.

## 🧾 License  
This project is licensed under the **MIT License**, allowing free use, modification, and redistribution with attribution.
