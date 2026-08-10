from src.langgraphagenticai.state.state import State

class BasicChatbotNode:

    """
        Basic Chatbot login implementation
    """

    def __init__(self, model):
        self.llm = model

    def process(self, state:State)->dict:
        """
        Docstring for process: process the input state and generate a chatbot response
        """
        return {'messages': self.llm.invoke(state['messages'])}