import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


class DisplayResultsStreamlit:
    def __init__(self,usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message
        
    def display_results_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        
        if usecase == "Basic ChatBot":
            # Create proper HumanMessage object
            human_message = HumanMessage(content=user_message)
            
            # Display user message first
            with st.chat_message("user"):
                st.write(user_message)
            
            # Stream the graph response
            for event in graph.stream({"messages": [human_message]}):
                for value in event.values():
                    if 'messages' in value:
                        with st.chat_message("assistant"):
                            st.write(value['messages'].content)
                            
                            
        elif usecase == "Chatbot with Web":
            
            initial_state = {"messages": [HumanMessage(content=user_message)]}
            res = graph.invoke(initial_state)
            for message in res['messages']:
                if type(message) == HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)
                elif type(message) == ToolMessage:
                    with st.chat_message("ai"):
                        st.write("Tool call start")
                        st.write(message.content)
                        st.write("Tool call end")
                        
                elif type(message) == AIMessage and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)
                        
        
        elif usecase == "AI News":
            frequency = self.user_message
            with st.spinner("Fetching and processing AI news..."):
                result = graph.invoke({"messages": frequency})
                try:
                    AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH,'r') as file:
                        markdown_content = file.read()
                        
                        # Display the markdown content
                        st.markdown(markdown_content, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error("Error: Summary file not found.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")