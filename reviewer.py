import docx
import os
import openai

# Set your OpenAI API Key
openai.api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Required document names
REQUIRED_DOCUMENTS = [
    "Articles of Association",
    "Resolution of Incorporating Shareholders",
    "Register of Members and Directors",
    "Share Capital",
    "Appointment of Director(s)"
]

def review_docx(file_path, doc_type, total_uploaded, uploaded_names):
    # Load .docx
    try:
        doc = docx.Document(file_path)
    except Exception as e:
        return {"error": f"Failed to read {file_path}: {str(e)}"}

    # Extract all clauses (paragraphs)
    clauses = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    # Detect found documents by scanning content
    file_text = " ".join(clauses)
    found_docs = []
    for req in REQUIRED_DOCUMENTS:
        if req.lower() in file_text.lower():
            found_docs.append(req)

    # Missing documents
    missing_docs = [doc for doc in REQUIRED_DOCUMENTS if doc not in found_docs]
    missing_docs = missing_docs if missing_docs else None

    # Send clauses to OpenAI for review
    issues = []
    for idx, clause in enumerate(clauses, start=1):
        try:
            prompt = f"""
            You are an ADGM legal compliance checker.
            Review the following clause for compliance issues with ADGM rules:

            Clause: {clause}

            If there is an issue, respond in JSON:
            {{
                "issue": "...",
                "severity": "High/Medium/Low",
                "suggestion": "..."
            }}

            If no issue, respond with: null
            """
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            content = response.choices[0].message["content"].strip()
            if content.lower() != "null":
                import json
                issues.append({
                    "document": os.path.basename(file_path),
                    "section": f"Clause {idx}",
                    **json.loads(content)
                })
        except Exception as e:
            issues.append({
                "document": os.path.basename(file_path),
                "section": f"Clause {idx}",
                "issue": f"Error reviewing clause: {str(e)}",
                "severity": "Error",
                "suggestion": "Check manually"
            })

    # Final structured output
    return {
        "process": doc_type,
        "documents_uploaded": total_uploaded,
        "required_documents": len(REQUIRED_DOCUMENTS),
        "missing_document": missing_docs,
        "issues_found": issues
    }
