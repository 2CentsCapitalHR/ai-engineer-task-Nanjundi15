import gradio as gr
from core import reviewer
import os

def review_files(files, doc_type):
    if not isinstance(files, list):
        files = [files] if files else []

    uploaded_names = [os.path.basename(f) for f in files]
    results = []

    for f in files:
        results.append(reviewer.review_docx(f, doc_type, len(files), uploaded_names))

    return results if len(results) > 1 else results[0] if results else {}

css = """
body {
    background: linear-gradient(135deg, #4B6CB7 0%, #182848 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h1, h2, h3, h4 {
    color: white !important;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.7);
    font-weight: 700;
}
.gradio-container {
    max-width: 900px !important;
    margin: auto !important;
    padding: 25px !important;
    background-color: rgba(255,255,255,0.1);
    border-radius: 15px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
.gr-button {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 12px rgba(118,75,162,0.6);
    transition: background 0.3s ease;
}
.gr-button:hover {
    background: linear-gradient(90deg, #764ba2 0%, #667eea 100%) !important;
}
.gr-file label, .gr-textbox label {
    color: #dcd6f7 !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
}
.gr-file input[type="file"] {
    border-radius: 10px !important;
    border: 1.5px solid #aba7de !important;
    padding: 8px !important;
    background-color: rgba(255,255,255,0.9) !important;
}
.gr-textbox textarea, .gr-textbox input {
    border-radius: 10px !important;
    border: 1.5px solid #aba7de !important;
    padding: 10px !important;
    font-size: 1rem !important;
    background-color: rgba(255,255,255,0.95) !important;
    color: #333 !important;
}
.gr-json {
    background-color: rgba(255,255,255,0.9) !important;
    border-radius: 12px !important;
    padding: 15px !important;
    font-family: 'Courier New', Courier, monospace !important;
    max-height: 400px !important;
    overflow-y: auto !important;
    box-shadow: 0 0 12px rgba(0,0,0,0.15);
}
"""

with gr.Blocks(css=css) as demo:
    gr.Markdown("<h1 style='text-align: center;'>📑 ADGM Compliance Reviewer</h1>")
    gr.Markdown("<p style='text-align:center; font-size:18px; color:#ddd;'>Upload your <strong>ADGM-related .docx documents</strong> and get structured compliance feedback instantly.</p>")

    with gr.Row():
        file_input = gr.File(
            file_types=[".docx"],
            type="filepath",
            label="📂 Upload .docx File(s)",

        )

        doc_type_input = gr.Textbox(
            label="Document Type",
            placeholder="e.g. Company Incorporation"
        )

    review_button = gr.Button("🔍 Review Document", variant="primary")
    output = gr.JSON(label="📋 Review Results")

    review_button.click(
        review_files,
        inputs=[file_input, doc_type_input],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch()
