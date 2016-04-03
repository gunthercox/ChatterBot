from .conversation import Statement
from .corpus import Corpus


class Trainer(object):

    def __init__(self, storage, **kwargs):
        self.storage = storage
        self.corpus = Corpus()

    def train_from_list(self, conversation):
        recent_statements = []

        for text in conversation:
            statement = self.storage.find(text)

            # Create the statement if a match was not found
            if not statement:
                statement = Statement(text)

            previous_statement = None
            if recent_statements:
                previous_statement = recent_statements[-1]

            if previous_statement:
                statement.add_response(previous_statement)

            recent_statements.append(statement)
            self.storage.update(statement)

    def train_from_corpora(self, corpora):
        for corpus in corpora:
            corpus_data = self.corpus.load_corpus(corpus)
            for data in corpus_data:
                for pair in data:
                    self.train_from_list(pair)
