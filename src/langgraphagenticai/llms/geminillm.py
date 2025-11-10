import os
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI


class GeminiLLM:
    def __init__(self,user_controls_input):
        self.user_controls_input = user_controls_input
        
    def get_llm_model(self):
        try:
            google_api_key = self.user_controls_input.get("gemini_api_key", "")
            selected_gemini_model = self.user_controls_input.get("selected_gemini_model", "")
            
            if not google_api_key and not os.environ.get('GOOGLE_API_KEY'):
                st.error("Please enter the Google API KEY") 
                return None
            
            llm = ChatGoogleGenerativeAI(
                api_key=google_api_key or os.environ.get('GOOGLE_API_KEY'),
                model=selected_gemini_model
            )
            
        except Exception as e:
            raise ValueError(f"Error initializing Gemini LLM: {e}")
        
        return llm
    

    