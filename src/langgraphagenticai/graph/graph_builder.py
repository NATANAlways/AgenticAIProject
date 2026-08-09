from langgraph.graph import StateGraph
from src.langgraphagenticai.state import State
from langgraph.graph import StateGraph, START, END

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Docstring for basic_chatbot_build_graph
        
        Builds a basic chatbot graph using LangGraph
        this method initalise a chatbot node using the BasicChatBotNode class
        and integrate it into the graph. The chatbot node is set as both the entry 
        and exit point of the graph

        """

        self.graph_builder.add_node("chatbot","")
        self.graph_builder.add_edge(START, "")
