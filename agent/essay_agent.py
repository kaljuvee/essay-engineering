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
    original_text: str
    current_version: int
    is_new_student: bool
    current_step: str  # 'intro', 'meaning_blocks', 'reconstruction', 'feedback'
    student_meaning_blocks: str
    confirmed_meaning_blocks: str

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
            # Check if student is new or unsure
            if "have you used" in student_blocks.lower() or "i don't know" in student_blocks.lower():
                return f"""Welcome! Let me explain the Essay Engineering method.

We'll work with this sentence:
"{original_text}"

Let's begin with Step 1: Break it into meaning blocks.

Can you tell me:
1. How many different meaning blocks do you think there are in this sentence?
2. Where would you put the parentheses to separate them?

Just give me your division into meaning blocks first. Once we confirm that, we'll move on to version 1 (v1) of your meaning reconstruction."""
            
            # Check if student has provided meaning blocks
            if "(" in student_blocks and ")" in student_blocks:
                # Analyze the meaning blocks
                blocks = student_blocks.strip("()").split(")(")
                
                # Check if blocks form a complete sentence
                if len(blocks) > 1:
                    return f"""Thanks — that's a good start. Let's refine the division based on the core principle of the Essay Engineering method: semantic grouping — what ideas belong together in terms of meaning.

Here's how we can analyze it:

Original Sentence:
"{original_text}"

Let's apply the main rule: when different phrases all contribute to a single general idea or action, they stay in the same meaning block.

In this case, the whole sentence expresses a single action and its context. Everything supports the central idea of what the Mole was doing.

Correct Meaning Block:
({original_text})

Now that we've locked in the meaning block, you're ready to write version 1 (v1) of your meaning reconstruction — just remember:

Don't repeat any words from the original sentence (except names of people or places).

It's fine if it's not perfect — just aim to capture some part of the meaning in your own words.

Go ahead and give me your v1!"""
                else:
                    return "Good! You've identified a single meaning block. Now, let's move on to reconstructing its meaning. Give me your v1!"
            
            return """When looking for meaning blocks, consider:
1. What is the main action or event?
2. Who is involved?
3. When does it happen?
4. Why or how is it happening?

Try breaking the text into these elements. For example, in the sentence:
"The Mole had been working very hard all the morning, spring-cleaning his little home."

You might identify blocks like:
(The Mole had been working very hard) (all the morning) (spring-cleaning his little home)

Give it a try with the current sentence!"""

        def evaluate_reconstruction(student_reconstruction: str, original_block: str) -> str:
            """Evaluate student's meaning reconstruction and provide feedback."""
            # Check for repeated words
            original_words = set(original_block.lower().split())
            student_words = set(student_reconstruction.lower().split())
            repeated_words = original_words.intersection(student_words)
            
            if repeated_words:
                return f"I notice you've used some words from the original text: {', '.join(repeated_words)}. Try to express the meaning without repeating any words from the original."
            
            # Calculate accuracy (this would be more sophisticated in practice)
            accuracy = 70  # Placeholder for actual accuracy calculation
            
            feedback = f"Your reconstruction is about {accuracy}% accurate. "
            if accuracy < 30:
                feedback += "You're on the right track, but try to capture more of the original meaning."
            elif accuracy < 60:
                feedback += "Good effort! You're getting closer to the core meaning."
            elif accuracy < 90:
                feedback += "Very good! You've captured most of the meaning. Can you refine it further?"
            else:
                feedback += "Excellent! You've captured the meaning very well."
            
            return feedback

        def provide_hints(original_text: str) -> str:
            """Provide hints to help students identify meaning blocks."""
            return """When looking for meaning blocks, consider:
1. What is the main action or event?
2. Who is involved?
3. When does it happen?
4. Why or how is it happening?

Try breaking the text into these elements. For example, in the sentence:
"The Mole had been working very hard all the morning, spring-cleaning his little home."

You might identify blocks like:
(The Mole had been working very hard) (all the morning) (spring-cleaning his little home)

Give it a try with the current sentence!"""

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
            
            # Check if this is a new student or unsure
            if state["is_new_student"] or "i don't know" in latest_message.lower():
                state["is_new_student"] = False
                state["current_step"] = "intro"
                result = self.tools[0].invoke({
                    "student_blocks": latest_message,
                    "original_text": state["original_text"]
                })
                state["current_meaning_block"] = result
                return state
            
            # Check if this is a meaning block identification
            if "(" in latest_message and ")" in latest_message:
                state["current_step"] = "meaning_blocks"
                state["student_meaning_blocks"] = latest_message
                result = self.tools[0].invoke({
                    "student_blocks": latest_message,
                    "original_text": state["original_text"]
                })
                state["current_meaning_block"] = result
                return state
            
            # Check if this is a reconstruction attempt
            if "v" in latest_message.lower() or any(str(i) in latest_message for i in range(1, 10)):
                state["current_step"] = "reconstruction"
                state["current_version"] += 1
                result = self.tools[1].invoke({
                    "student_reconstruction": latest_message,
                    "original_block": state["original_text"]
                })
                state["reconstruction_versions"].append(latest_message)
                state["current_meaning_block"] = result
                return state
            
            # Default to providing hints
            result = self.tools[2].invoke({
                "original_text": state["original_text"]
            })
            state["current_meaning_block"] = result
            return state

        def provide_guidance(state: EssayState) -> EssayState:
            """Provide additional guidance if needed."""
            if not state["current_meaning_block"]:
                return state
            
            # Check if student might need hints
            if "help" in state["current_meaning_block"].lower() or "hint" in state["current_meaning_block"].lower():
                result = self.tools[2].invoke({
                    "original_text": state["original_text"]
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
            # Extract original text from first message if it contains a quote
            original_text = ""
            for msg in messages:
                if '"' in msg["content"]:
                    # Extract text between quotes
                    start = msg["content"].find('"') + 1
                    end = msg["content"].rfind('"')
                    if start > 0 and end > start:
                        original_text = msg["content"][start:end]
                        break
            
            # Initialize state
            initial_state = EssayState(
                messages=messages,
                current_meaning_block="",
                reconstruction_versions=[],
                accuracy_scores=[],
                original_text=original_text,
                current_version=0,
                is_new_student=True,
                current_step="intro",
                student_meaning_blocks="",
                confirmed_meaning_blocks=""
            )
            print(f"[DEBUG] Initial state: {initial_state}")
            
            # Run the graph
            for state in self.graph.stream(initial_state):
                print(f"[DEBUG] State from graph: {state}")
                node_state = list(state.values())[0] if state else {}
                
                # Yield reconstruction versions if available
                if "reconstruction_versions" in node_state and node_state["reconstruction_versions"]:
                    latest_reconstruction = node_state["reconstruction_versions"][-1]
                    print(f"[DEBUG] Yielding: {latest_reconstruction}")
                    yield latest_reconstruction + " "
                
                # Yield current meaning block if available
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
