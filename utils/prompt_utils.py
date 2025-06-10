from typing import Dict
from .pdf_utils import load_pdf_contexts

def get_system_prompt_with_contexts() -> str:
    """
    Generate the system prompt with PDF contexts included.
    
    Returns:
        str: System prompt with PDF contexts
    """
    # Load PDF contexts
    pdf_contexts = load_pdf_contexts()
    
    # Base system prompt
    base_prompt = """You are Essay Engineering Tutor, an expert reading-comprehension and essay-writing coach.
Your single goal is to help a student reach 90–100 % accuracy and completeness in understanding prose one sentence at a time and to turn that understanding into strong analytical writing.

The following PDF documents have been provided as context for your responses:
"""
    
    # Add PDF contexts
    for filename, content in pdf_contexts.items():
        base_prompt += f"\n\n--- Content from {filename} ---\n{content}\n"
    
    return base_prompt 