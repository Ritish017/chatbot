import streamlit as st
from .ui.streamlit.loadui import LoadStreamlitUI
from .llms.groqllm import GroqLLM
from .llms.geminillm import GeminiLLM
from .graph.graph_builder import GraphBuilder
from .ui.streamlit.display_results import DisplayResultsStreamlit


def load_langgraph_agenticai_app():
    
    """
    Loads and runs the LangGraph Agentic AI Streamlit application.
    This function initializes the Streamlit UI and handles the application's execution.
    It should be called to start the LangGraph Agentic AI application.

    
    """
    
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    
    if not user_input:
        st.error("Error loading UI components. Please check the configuration.")
        return 
 
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.time_frame
    else:
        user_message = st.chat_input("Enter your message here:")
    
    if user_message:
        try:
            obj_llm_config = GroqLLM(user_controls_input=user_input) if user_input["selected_llm"]=="Groq" else GeminiLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()
            
            if not model:
                st.error("Error: LLM model could not initialized")
                
            usecase = user_input.get("selected_usecase")
            
            if not usecase:
                st.error("Error: Usecase not selected")
                return
            
            graph_builder = GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultsStreamlit(usecase, graph, user_message).display_results_on_ui()
            except Exception as e:
                st.error(f"Error setting up graph: {e}")
                return
            
        except Exception as e:
            st.error(f"Error setting up graph: {e}")
            return
        
        
            
        
    