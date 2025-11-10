from typing_extensions import TypedDict, Literal, List
from langgraph.graph.message import add_messages
from typing import Annotated

class State(TypedDict):
    """
    Represnt the structure of the state used in graph
    """
    
    messages : Annotated[List, add_messages]