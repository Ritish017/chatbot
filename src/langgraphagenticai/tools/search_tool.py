from langchain_community.tools import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools():
    """
    Returns the list of tools to be used in chatbot
    
    """
    
    tools = [TavilySearchResults(max_results=2)]
    return tools


def create_tool_node(tools):
    """
    creates and returns tool node for the graph
    """
    
    return ToolNode(tools=tools)