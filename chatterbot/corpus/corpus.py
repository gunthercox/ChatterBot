import os


class Corpus(object):

    def __init__(self):
        current_directory = os.path.dirname(__file__)
        self.data_directory = os.path.join(current_directory, 'data')

    def get_file_path(self, dotted_path):
        """
        Reads a dotted file path and returns the file path.
        """
        parts = dotted_path.split(".")
        if parts[0] == 'chatterbot':
            parts.pop(0)
            parts[0] = self.data_directory

        corpus_path = os.path.join(*parts)

        if os.path.exists(corpus_path + ".json"):
            corpus_path += ".json"

        return corpus_path

    def read_corpus(self, file_name):
        """
        Read and return the data from a corpus json file.
        """
        import json

        with open(file_name) as data_file:
            data = json.load(data_file)
        return data

    def load_corpus(self, dotted_path):
        """
        Return the data contained within a specified corpus.
        """

        corpus_path = self.get_file_path(dotted_path)

        corpora = []

        if os.path.isdir(corpus_path):
            for dirname, dirnames, filenames in os.walk(corpus_path):
                for datafile in filenames:
                    if datafile.endswith(".json"):

                        corpus = self.read_corpus(
                            os.path.join(dirname, datafile)
                        )

                        for key in list(corpus.keys()):
                            corpora.append(corpus[key])
        else:
            corpus = self.read_corpus(corpus_path)

            for key in list(corpus.keys()):
                corpora.append(corpus[key])

        return corpora
