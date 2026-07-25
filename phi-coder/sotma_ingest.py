
import os
import json
import fitz  # PyMuPDF
from pathlib import Path

SOURCE_DIR = r"C:\Users\Andrew\ollama\phi-coder\S.O.T.M.A"
OUTPUT_JSONL = "sotma_dataset.jsonl"
INGEST_LOG = "sotma_ingest_log.json"

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()

def chunk_text(text, max_length=1000):
    paragraphs = text.split("\n")
    chunks = []
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) < max_length:
            current_chunk += para + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def build_dataset_entry(prompt, response):
    return {"prompt": prompt, "response": response}

def main():
    entries = []
    ingest_log = []
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                full_path = os.path.join(root, file)
                try:
                    text = extract_text_from_pdf(full_path)
                    if not text:
                        continue
                    chunks = chunk_text(text)
                    for i, chunk in enumerate(chunks):
                        prompt = f"What does the SOTMA document '{file}' say (part {i+1})?"
                        entry = build_dataset_entry(prompt, chunk)
                        entries.append(entry)
                    ingest_log.append({"file": file, "chunks": len(chunks), "path": full_path})
                except Exception as e:
                    ingest_log.append({"file": file, "error": str(e)})
    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")
    with open(INGEST_LOG, "w", encoding="utf-8") as f:
        json.dump(ingest_log, f, indent=2)
    print(f"Processed {len(entries)} chunks from SOTMA.")

if __name__ == "__main__":
    main()
