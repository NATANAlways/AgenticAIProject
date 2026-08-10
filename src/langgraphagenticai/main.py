import streamlit as st

from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.llm.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.displayresult import DisplayResultStreamlit

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

    if user_message:
        try:
            ## Configure the LLM's
            obj_llm_config = GroqLLM(user_controls_iput=user_input)
            model = obj_llm_config.get_llm_models()

            if not model:
                st.error("Error: LLm model could not be initialized")
                return
            
            # Initialize and setup the graph based use case
            usecase = user_input.get("selected_usecase")

            if not usecase:
                st.error("Error: No use case selected.")
                return
            
            # Graph Builder
            graph_builder = GraphBuilder(model=model)
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Graph setup failed - {e}")
                return

        except Exception as e:
            st.error(f"Error: Graph set up failed- {e}")
            return 


