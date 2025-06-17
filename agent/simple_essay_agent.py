from typing import List, Dict, Optional
from dataclasses import dataclass
import json

@dataclass
class Message:
    role: str
    content: str

@dataclass
class MeaningBlock:
    text: str
    explanation: str

class SimpleEssayAgent:
    def __init__(self):
        self.conversation_history: List[Message] = []
        self.current_sentence: Optional[str] = None
        self.meaning_blocks: List[MeaningBlock] = []
        self.versions: List[str] = []
        
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history."""
        self.conversation_history.append(Message(role=role, content=content))
        
    def analyze_meaning_blocks(self, sentence: str) -> List[MeaningBlock]:
        """Analyze a sentence and break it into meaning blocks."""
        self.current_sentence = sentence
        
        # Simple heuristic: split on commas and conjunctions
        parts = sentence.replace(",", " , ").replace("even", " even ").split()
        blocks = []
        current_block = []
        
        for part in parts:
            current_block.append(part)
            if part in [",", "even"]:
                blocks.append(" ".join(current_block).strip())
                current_block = []
                
        if current_block:
            blocks.append(" ".join(current_block).strip())
            
        # Create meaning blocks with simple explanations
        self.meaning_blocks = [
            MeaningBlock(
                text=block,
                explanation=f"This block expresses {self._get_block_type(block)}"
            )
            for block in blocks
        ]
        
        return self.meaning_blocks
    
    def _get_block_type(self, block: str) -> str:
        """Determine the type of meaning in a block."""
        if "touch" in block.lower():
            return "a subtle presence or quality"
        elif "paternal" in block.lower():
            return "a father-like attitude"
        elif "contempt" in block.lower():
            return "a feeling of disdain or superiority"
        elif "people he liked" in block.lower():
            return "the scope of the attitude extending to friends"
        return "a part of the overall meaning"
    
    def create_version(self, version_num: int, text: str):
        """Add a new version of the meaning reconstruction."""
        self.versions.append(f"v{version_num}. {text}")
        
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation and analysis."""
        summary = []
        
        if self.current_sentence:
            summary.append(f"Original sentence: {self.current_sentence}\n")
            
        if self.meaning_blocks:
            summary.append("Meaning blocks:")
            for block in self.meaning_blocks:
                summary.append(f"- {block.text}")
                summary.append(f"  {block.explanation}")
            summary.append("")
            
        if self.versions:
            summary.append("Versions:")
            for version in self.versions:
                summary.append(version)
                
        return "\n".join(summary)
    
    def get_next_prompt(self) -> str:
        """Generate the next prompt based on the current state."""
        if not self.current_sentence:
            return "Please provide a sentence to analyze."
            
        if not self.meaning_blocks:
            return "Let's analyze the meaning blocks in this sentence. How would you divide it?"
            
        if not self.versions:
            return "Now that we have the meaning blocks, try creating version 1 (v1) of your meaning reconstruction. Remember not to repeat words from the original."
            
        last_version = self.versions[-1]
        version_num = len(self.versions)
        
        return f"Thanks for v{version_num}. Let's improve it. Think about:\n" + \
               "1. Is the emotional tone accurate?\n" + \
               "2. Are you capturing the subtle meaning?\n" + \
               "3. Are you avoiding repetition?\n" + \
               f"Try v{version_num + 1}."
