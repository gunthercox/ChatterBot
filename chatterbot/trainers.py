from .conversation import Statement, Response
from .corpus import Corpus


class Trainer(object):

    def __init__(self, storage, **kwargs):
        self.storage = storage
        self.corpus = Corpus()

    def train(self, *args, **kwargs):
        raise self.TrainerInitializationException()

    class TrainerInitializationException(Exception):

        def __init__(self, value='A training class must be set using the `set_trainer` method before calling `train()`.'):
            self.value = value

        def __str__(self):
            return repr(self.value)

    def _generate_export_data(self):
        result = []

        for statement in self.storage.filter():
            for response in statement.in_response_to:
                result.append([response.text, statement.text])

        return result

    def export_for_training(self, file_path='./export.json'):
        """
        Create a file from the database that can be used to
        train other chat bots.
        """
        from jsondb.db import Database
        database = Database(file_path)
        export = {'export': self._generate_export_data()}
        database.data(dictionary=export)


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
