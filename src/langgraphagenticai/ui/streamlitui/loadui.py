import streamlit as st
import os

from src.langgraphagenticai.ui.uiconfig import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title = "### " + self.config.get_page_title(), layout="wide")
        st.header(" ### " + self.config.get_page_title())

        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()
            
            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("select LLM", llm_options)
            
            if self.user_controls["selected_llm"] == 'Groq':
                # Model Selection
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API key", type="password")
                #validate API key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning(" Please enter your GROQ API key to proceed. Don't have ? refer: https://console.groq.com/keys")
            
            ## use case selection
            self.user_controls["selected_usecase"] = st.selectbox("select usecase", usecase_options)

            if self.user_controls["selected_usecase"] == "Chatbot with web" or self.user_controls["selected_usecase"] == "AI News":
                os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("TAVILY API KEY", type="password")

                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please enter your TAVILY_API_KEY key to proceedd. Don't have? refer : https://app.tavily.com/keys")

            if self.user_controls["selected_usecase"] == "AI News":
                st.subheader(" AI News Explorer")

                with st.sidebar:
                    time_frame = st.selectbox(
                        "Select Time Frame",
                        ["Daily", "Weekly", "Monthly"],
                        index = 0
                    )

                if st.button("Fetch Latest AI News", width="stretch"):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame

        return self.user_controls
            