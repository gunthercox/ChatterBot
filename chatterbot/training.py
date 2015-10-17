from .corpus.utils import load_corpus
from .conversation import Statement


class Trainer(object):

    def __init__(self, chatbot, **kwargs):
        self.chatbot = chatbot

    def train_from_list(self, conversation):

        recent_statements = []

        for text in conversation:
            statement = self.chatbot.storage.find(text)

            # Create the statement if a match was not found
            if not statement:
                statement = Statement(text)

            previous_statement = None
            if recent_statements:
                previous_statement = recent_statements[-1]

            if previous_statement:
                statement.add_response(previous_statement)

            recent_statements.append(statement)
            self.chatbot.storage.update(statement)

    def train_from_corpora(self, corpora):
        for corpus in corpora:
            corpus_data = load_corpus(corpus)
            for data in corpus_data:
                for pair in data:
                    self.train_from_list(pair)

