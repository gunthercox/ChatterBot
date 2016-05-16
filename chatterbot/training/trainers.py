from chatterbot.conversation import Statement
from chatterbot.corpus import Corpus


class Trainer(object):

    def __init__(self, storage, **kwargs):
        self.kwargs = kwargs
        self.storage = storage
        self.corpus = Corpus()

    def train(self):
        pass


class ListTrainer(Trainer):

    def train(self, conversation):
        statement_history = []

        for text in conversation:
            statement = self.storage.find(text)

            # Create the statement if a match was not found
            if not statement:
                statement = Statement(text)

            previous_statement = None
            if statement_history:
                previous_statement = statement_history[-1]

            if previous_statement:
                statement.add_response(previous_statement)

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
