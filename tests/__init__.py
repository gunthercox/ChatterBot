from chatterbot import ChatBot
from chatterbot import comparisons
from chatterbot.logic import LogicAdapter


def setup_module():
    chatbot = ChatBot('setup')

    chatbot.logic_adapters = [
        LogicAdapter(
            chatbot,
            statement_comparison_function=comparisons.jaccard_similarity
        ),
        LogicAdapter(
            chatbot,
            statement_comparison_function=comparisons.sentiment_comparison
        ),
        LogicAdapter(
            chatbot,
            statement_comparison_function=comparisons.synset_distance
        ),
    ]

    chatbot.initialize()
