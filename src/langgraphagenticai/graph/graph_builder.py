from langgraph.graph import StateGraph,START,END
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition, ToolNode
from src.langgraphagenticai.nodes.chatbot_with_tol_node import ChatbotWithTolNode
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode



class GraphBuilder:
    def __init__(self,model):
        self.llm = model
        self.graph_builder = StateGraph(State)
        
    def basic_chatbot_graph(self):
        """
        Build a basic chatbot graph using Langgraph
        This method intializes a chatbot node using the BasicChatBotGraph class
        and integrates it inot the graph.The chatbot node os set as both the 
        entry and exit point of the graph.
        """
        
        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)
        
        
        
    def chatbot_with_tools_build_graph(self):
        """
        Builds an Advanced chatbot graph using Langgraph with tool integration.
        This method initializes a Chatbot graph that includes botha chatbot node
        and tool node. It defines tools, initializes the chatbot with tool
        capabilities, and sets up the graph structure to incorporate these nodes.
        The chatbot node is set as the entry point.
        """
        
        tools = get_tools()
        tool_node = create_tool_node(tools)
        llm = self.llm
        
        obj_chatbot_node = ChatbotWithTolNode(llm)
        
        self.graph_builder.add_node("Chatbot",obj_chatbot_node.create_chatbot(tools))
        self.graph_builder.add_node("tools",tool_node)
        
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges(
            "chatbot",
            tools_condition
            
        )
        
        self.graph_builder.add_edge("tools","chatbot")
        self.graph_builder.add_edge("chatbot",END)
        
        
        
    def ai_news_builder_graph(self):
        
        ai_news_node = AINewsNode(self.llm)
        
        
        
        """
        
        """
        
        self.graph_builder.add_node("fetch_news",ai_news_node.fetch_news)
        
        self.graph_builder.add_node("summarize_news",ai_news_node.summarize_news)
        self.graph_builder.add_node("save_results",ai_news_node.save_results)
        
        
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news","summarize_news")
        self.graph_builder.add_edge("summarize_news","save_results")
        
        
        
    def setup_graph(self,usecase: str):
        """
        sets up the graph for teh selected use case
        """
        
        if usecase == "Basic ChatBot":
            self.basic_chatbot_graph()
            
        if usecase == "Chatbot with Web":
            self.chatbot_with_tools_build_graph()
            
        if usecase == "AI News":
            self.ai_news_builder_graph()
            
        return self.graph_builder.compile()
    
    

    