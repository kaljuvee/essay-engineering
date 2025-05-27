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
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.llm = ChatOpenAI(model=self.model, temperature=0.7)
        self.default_system_prompt = """You are an essay writing tutor. Help students improve their writing by identifying meaning blocks, reconstructing meaning, and providing feedback."""
        self.tools = self._create_tools()
        self.graph = self._create_graph()
        self.memory = MemorySaver()
    
    def _create_tools(self) -> List[Any]:
        """Create tools for the agent."""
        def identify_meaning_blocks(text: str) -> str:
            """Identify meaning blocks in a given text."""
            return "Great! You've identified the meaning blocks correctly. Here they are:\n1. 'The Mole had been working very hard'\n2. 'all the morning'\n3. 'spring-cleaning his little home'\n\nNow, let's reconstruct the meaning of each block."

        def evaluate_accuracy(reconstruction: str, original: str) -> float:
            """Evaluate the accuracy of a meaning reconstruction and return a numeric score (0.0 to 1.0)."""
            # Simulate accuracy evaluation (replace with actual logic)
            return 0.8  # Example: 80% accuracy

        def compare_versions(versions: List[str]) -> str:
            """Compare different versions of meaning reconstruction."""
            return "The versions are similar, but the second version emphasizes the seasonal aspect of spring-cleaning."

        return [
            Tool.from_function(identify_meaning_blocks, name="identify_meaning_blocks", description="Identify meaning blocks in a given text."),
            StructuredTool.from_function(evaluate_accuracy, name="evaluate_accuracy", description="Evaluate the accuracy of a meaning reconstruction and return a numeric score (0.0 to 1.0)."),
            Tool.from_function(compare_versions, name="compare_versions", description="Compare different versions of meaning reconstruction.")
        ]
    
    def _create_graph(self) -> StateGraph:
        """Create the LangGraph workflow."""
        # Define the nodes
        def process_input(state: EssayState) -> EssayState:
            """Process the input and identify meaning blocks."""
            messages = state["messages"]
            if not messages:
                return state
            
            # Get the latest message
            latest_message = messages[-1]["content"]
            
            # Use the identify_meaning_blocks tool
            result = self.tools[0].invoke({"text": latest_message})
            
            # Update state with identified meaning blocks
            state["current_meaning_block"] = result
            return state

        def generate_reconstruction(state: EssayState) -> EssayState:
            """Generate a meaning reconstruction."""
            if not state["current_meaning_block"]:
                return state
            
            # Create prompt for reconstruction
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.default_system_prompt),
                ("human", "Please reconstruct the meaning of this block: {block}")
            ])
            
            # Generate reconstruction
            chain = prompt | self.llm | StrOutputParser()
            reconstruction = chain.invoke({"block": state["current_meaning_block"]})
            
            # Add to versions
            state["reconstruction_versions"].append(reconstruction)
            return state

        def evaluate_reconstruction(state: EssayState) -> EssayState:
            """Evaluate the latest reconstruction."""
            if not state["reconstruction_versions"]:
                return state
            
            # Use the evaluate_accuracy tool
            latest_reconstruction = state["reconstruction_versions"][-1]
            result = self.tools[1].invoke({
                "reconstruction": latest_reconstruction,
                "original": state["current_meaning_block"]
            })
            
            # Update accuracy scores
            state["accuracy_scores"].append(result)  # result is already a float
            return state

        # Create the graph
        workflow = StateGraph(EssayState)
        
        # Add nodes
        workflow.add_node("process_input", process_input)
        workflow.add_node("generate_reconstruction", generate_reconstruction)
        workflow.add_node("evaluate_reconstruction", evaluate_reconstruction)
        
        # Add edges
        workflow.add_edge(START, "process_input")
        workflow.add_edge("process_input", "generate_reconstruction")
        workflow.add_edge("generate_reconstruction", "evaluate_reconstruction")
        workflow.add_edge("evaluate_reconstruction", END)
        
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
