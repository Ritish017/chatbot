import os
import streamlit as st

from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self,user_controls_input):
        self.user_controls_input = user_controls_input
        
        
    def get_llm_model(self):
        try:
            groq_api_key = self.user_controls_input.get("groq_api_key", "")
            selected_groq_model = self.user_controls_input.get("selected_groq_model", "")

            if not groq_api_key and not os.environ.get('GROQ_API_KEY'):
                st.error("Please enter the GROQ API KEY")
                return None

            llm = ChatGroq(
                api_key=groq_api_key or os.environ.get('GROQ_API_KEY'),
                model=selected_groq_model
            )
        
        except Exception as e:
            raise ValueError(f"Error initializing Groq LLM: {e}")
        
        return llm
    