from .conversation import Statement, Response
from .corpus import Corpus


class Trainer(object):

    def __init__(self, storage, **kwargs):
        self.storage = storage
        self.corpus = Corpus()

    def train(self):
        pass


class ListTrainer(Trainer):

    def get_or_create(self, statement_text):
        """
        Return a statement if it exists.
        Create and return the statement if it does not exist.
        """
        statement = self.storage.find(statement_text)

        if not statement:
            statement = Statement(statement_text)

        return statement

    def train(self, conversation):
        statement_history = []

        for text in conversation:
            statement = self.get_or_create(text)

            if statement_history:
                statement.add_response(
                    Response(statement_history[-1].text)
                )

            statement_history.append(statement)
            self.storage.update(statement)


class ChatterBotCorpusTrainer(Trainer):

    def train(self, *corpora):
        trainer = ListTrainer(self.storage)

        for corpus in corpora:
            corpus_data = self.corpus.load_corpus(corpus)
            for data in corpus_data:
                for pair in data:
                    trainer.train(pair)
