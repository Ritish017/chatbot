from src.langgraphagenticai.state.state import State


class ChatbotWithTolNode:
    """
    State structure for Chatbot with Tools usecase
    """
    def __init__(self, model):
        self.llm = model
       
        
    def process(self, state:State) -> dict:
        """
        Process the state and return the response
        """
        
        # First, use the LLM to generate a response based on the messages
        user_input = state['messages'][-1] if state['messages'] else ""
        llm_response = self.llm.invoke({"role": "user", "content": user_input})
        
        
        tools_response  = f"Tool intgration for : '{user_input}'"
        
        return {"messages": [llm_response, tools_response]}
    
    
    def create_chatbot(self, tools):
        """Returns a chatbot instance with tool integration."""
        
        llm_with_tools = self.llm.bind_tools(tools)
        
        def chatbot_node(state: State) :
            """
            Chatbot logic forprocessing the inpit state and returning a response 
            """
            
            return {"messages": llm_with_tools.invoke(state['messages'])}
        
        return chatbot_node