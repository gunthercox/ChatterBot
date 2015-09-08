from .corpus.utils import read_corpus
from .conversation import Statement


class Trainer(object):

    def __init__(self, chatbot, **kwargs):
        self.chatbot = chatbot

        # TODO: If I just choose .english, it should recurse through all sub-modules of that corpus.
        default_corpora = [
            "chatterbot.corpus.english.greetings",
            "chatterbot.corpus.english.conversations"
        ]

        self.corpora = kwargs.get("corpora", default_corpora)

    def train_from_list(self, conversation):
        for text in conversation:
            statement = self.chatbot.storage.find(text)

            # Create the statement if a match was not found
            if not statement:
                statement = Statement(text)
            else:
                statement.update_occurrence_count()

            previous_statement = self.chatbot.get_last_statement()

            if previous_statement:
                statement.add_response(previous_statement)

            self.chatbot.recent_statements.append(statement)
            self.chatbot.storage.update(statement)

    def train_from_corpora(self):
        pass

