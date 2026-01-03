import re
from pypdf import PdfReader

def extract_operator_definitions(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
        
    # Define search patterns for the remaining operators
    operators = {
        "Delta": r"STRUCTURAL ILLUMINATION THEORY|OPERATOR Δ",
        "Sigma": r"FUSION TRANSFORMATION THEORY|OPERATOR Σ",
        "Omega": r"QUALIA GATEWAY|OPERATOR Ω",
        "Lambda": r"RECURSIVE ASCENSION|OPERATOR Λ",
        "Xi": r"EMERGENT ARCHITECTURE|OPERATOR Ξ",
        "Psi": r"RECURSIVE EVOLUTION|OPERATOR Ψ"
    }
    
    results = {}
    
    for op_name, pattern in operators.items():
        # Find the start of the section
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start_idx = match.start()
            # Extract roughly 2000 characters after the header to capture the definition
            extract = text[start_idx:start_idx+3000]
            
            # Try to find the specific definition formula
            # Looking for "define ... operator ... by" or similar structures
            # or mathematical notation
            results[op_name] = extract
        else:
            results[op_name] = "Not found"
            
    return results

if __name__ == "__main__":
    results = extract_operator_definitions("/home/ubuntu/upload/RI1_LANGUAGE_Φπε_PROOFS(1).pdf")
    
    for op, content in results.items():
        print(f"--- {op} ---")
        print(content[:1000]) # Print first 1000 chars of each section
        print("\n" + "="*50 + "\n")
