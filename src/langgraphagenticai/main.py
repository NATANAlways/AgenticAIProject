import streamlit as st

from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI

def load_langgraph_agentic_app():
    """
        Docstring for load_langgraph_agentic_app
        Load and runs the langgraph agentic ai application with stramlit UI.
        sets up the graph based on the selectd use case, and 
        displays the output while implementing exce[ption handling for robustness
    """

    # load ui
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI")
        return
    
    user_message = st.chat_input("Enter your message: ")

