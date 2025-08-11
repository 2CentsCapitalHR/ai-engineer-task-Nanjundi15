# 📑 ADGM Compliance Reviewer

A web app to review ADGM-related `.docx` documents for legal compliance issues using OpenAI's GPT models. Upload your documents, specify the document type, and get structured compliance feedback instantly.

---

## Features

- Upload single or multiple `.docx` files.
- Specify the document type (e.g., "Company Incorporation").
- Automated clause-by-clause review powered by OpenAI GPT.
- Highlights missing documents based on the provided type.
- Displays detailed JSON results with detected issues and suggestions.
- Beautiful, modern, responsive UI with custom styling using Gradio.

---

## Requirements

- Python 3.7+
- [Gradio](https://gradio.app/) (`pip install gradio`)
- [python-docx](https://python-docx.readthedocs.io/en/latest/) (`pip install python-docx`)
- OpenAI Python SDK version 1.x (`pip install openai`)

---

## Setup

1. Clone this repository or copy the code files.

2. Install dependencies:

```bash
pip install -r requirements.txt
