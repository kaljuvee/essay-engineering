import os
from typing import Dict
from PyPDF2 import PdfReader

def convert_pdf_to_text(pdf_path: str) -> str:
    """
    Convert a PDF file to text.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error converting PDF {pdf_path}: {str(e)}")
        return ""

def load_pdf_contexts(docs_dir: str = "docs") -> Dict[str, str]:
    """
    Load all PDF files from the docs directory and convert them to text.
    
    Args:
        docs_dir: Directory containing PDF files
        
    Returns:
        Dict[str, str]: Dictionary mapping PDF filenames to their text content
    """
    pdf_contexts = {}
    
    for filename in os.listdir(docs_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(docs_dir, filename)
            text = convert_pdf_to_text(pdf_path)
            if text:
                pdf_contexts[filename] = text
    
    return pdf_contexts 