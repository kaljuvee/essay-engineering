import os
from typing import List, Dict, Generator, Any, TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import Tool, StructuredTool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

class EssayState(TypedDict):
    messages: List[Dict[str, str]]
    current_meaning_block: str
    reconstruction_versions: List[str]
    accuracy_scores: List[float]

class EssayAgent:
    """Agent for essay writing assistance."""
    
    def __init__(self):
        """Initialize the essay agent."""
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.llm = ChatOpenAI(model=self.model, temperature=0.7)
        self.system_prompt = self._load_system_prompt()
        self.tools = self._create_tools()
        self.graph = self._create_graph()
        self.memory = MemorySaver()
    
    def _load_system_prompt(self) -> str:
        """Load the system prompt from file."""
        prompt_path = os.path.join("prompts", "system_prompt.md")
        try:
            with open(prompt_path, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise Exception(f"System prompt file not found at {prompt_path}")
    
    def _create_tools(self) -> List[Any]:
        """Create tools for the agent."""
        def evaluate_meaning_blocks(student_blocks: str, original_text: str) -> str:
            """Evaluate student's identified meaning blocks and provide feedback."""
            # This would be replaced with actual evaluation logic
            return "I see you've identified some meaning blocks. Could you explain why you chose to break the text this way? What makes each of these blocks meaningful?"

        def evaluate_reconstruction(student_reconstruction: str, original_block: str) -> str:
            """Evaluate student's meaning reconstruction and provide feedback."""
            # This would be replaced with actual evaluation logic
            return "Thank you for sharing your reconstruction. What aspects of the original text did you focus on in your interpretation? How does your reconstruction capture the key elements?"

        def provide_hints(original_text: str) -> str:
            """Provide hints to help students identify meaning blocks."""
            return "When looking for meaning blocks, consider: What are the main actions or events? Who is doing what? When is it happening? Try breaking the text into these elements."

        return [
            StructuredTool.from_function(
                evaluate_meaning_blocks,
                name="evaluate_meaning_blocks",
                description="Evaluate student's identified meaning blocks and provide feedback."
            ),
            StructuredTool.from_function(
                evaluate_reconstruction,
                name="evaluate_reconstruction",
                description="Evaluate student's meaning reconstruction and provide feedback."
            ),
            StructuredTool.from_function(
                provide_hints,
                name="provide_hints",
                description="Provide hints to help students identify meaning blocks."
            )
        ]
    
    def _create_graph(self) -> StateGraph:
        """Create the LangGraph workflow."""
        # Define the nodes
        def process_input(state: EssayState) -> EssayState:
            """Process student input and provide feedback."""
            messages = state["messages"]
            if not messages:
                return state
            
            # Get the latest message
            latest_message = messages[-1]["content"]
            
            # Check if this is a meaning block identification or reconstruction
            if "meaning blocks" in latest_message.lower():
                # Use the evaluate_meaning_blocks tool
                result = self.tools[0].invoke({
                    "student_blocks": latest_message,
                    "original_text": "The Mole had been working very hard all the morning, spring-cleaning his little home."
                })
            elif "reconstruction" in latest_message.lower():
                # Use the evaluate_reconstruction tool
                result = self.tools[1].invoke({
                    "student_reconstruction": latest_message,
                    "original_block": "The Mole had been working very hard all the morning, spring-cleaning his little home."
                })
            else:
                # Default to evaluating meaning blocks
                result = self.tools[0].invoke({
                    "student_blocks": latest_message,
                    "original_text": "The Mole had been working very hard all the morning, spring-cleaning his little home."
                })
            
            # Update state with feedback
            state["current_meaning_block"] = result
            return state

        def provide_guidance(state: EssayState) -> EssayState:
            """Provide additional guidance if needed."""
            if not state["current_meaning_block"]:
                return state
            
            # Check if student might need hints
            if "help" in state["current_meaning_block"].lower() or "hint" in state["current_meaning_block"].lower():
                result = self.tools[2].invoke({
                    "original_text": "The Mole had been working very hard all the morning, spring-cleaning his little home."
                })
                state["current_meaning_block"] = result
            
            return state

        # Create the graph
        workflow = StateGraph(EssayState)
        
        # Add nodes
        workflow.add_node("process_input", process_input)
        workflow.add_node("provide_guidance", provide_guidance)
        
        # Add edges
        workflow.add_edge(START, "process_input")
        workflow.add_edge("process_input", "provide_guidance")
        workflow.add_edge("provide_guidance", END)
        
        # Set entry point
        workflow.set_entry_point("process_input")
        
        return workflow.compile()
    
    def get_response(self, messages: List[Dict[str, str]], system_prompt: str = None) -> Generator[str, None, None]:
        """
        Get a streaming response from the agent.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            system_prompt: Optional system prompt to override the default one
            
        Yields:
            Chunks of the response as they arrive
        """
        if not messages:
            raise Exception("Messages list cannot be empty")
        print(f"[DEBUG] get_response called with messages: {messages}")
        try:
            # Initialize state
            initial_state = EssayState(
                messages=messages,
                current_meaning_block="",
                reconstruction_versions=[],
                accuracy_scores=[]
            )
            print(f"[DEBUG] Initial state: {initial_state}")
            # Run the graph
            for state in self.graph.stream(initial_state):
                print(f"[DEBUG] State from graph: {state}")
                node_state = list(state.values())[0] if state else {}
                if "reconstruction_versions" in node_state and node_state["reconstruction_versions"]:
                    latest_reconstruction = node_state["reconstruction_versions"][-1]
                    print(f"[DEBUG] Yielding: {latest_reconstruction}")
                    yield latest_reconstruction + " "
                elif "current_meaning_block" in node_state and node_state["current_meaning_block"]:
                    print(f"[DEBUG] Yielding current_meaning_block: {node_state['current_meaning_block']}")
                    yield node_state["current_meaning_block"] + " "
            print("[DEBUG] get_response finished streaming.")
        except Exception as e:
            print(f"[DEBUG] Exception in get_response: {e}")
            raise Exception(f"Graph execution error: {str(e)}")

    def reset_memory(self):
        """Reset the conversation memory."""
        self.memory.clear()
