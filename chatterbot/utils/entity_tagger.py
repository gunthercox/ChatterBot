import nltk

from chatterbot.utils.pos_tagger import POSTagger


class NamedEntityTagger():

    def __init__(self):
        """
        Constructor to initialize instance variables.
        """
        from nltk.data import find
        from nltk import download

        try:
            find('words.zip')
        except LookupError:
            download('words')

        try:
            find('maxent_ne_chunker.zip')
        except LookupError:
            download('maxent_ne_chunker')

        self.tagger = POSTagger()

    def ne_chunk(self, string):
        """
        Find all of the named entities and return them.
        """
        ne_list = []

        named_entities = nltk.ne_chunk(self.tagger.tag(self.tagger.tokenize(string)), binary=True)
        named_entities = nltk.chunk.tree2conlltags(named_entities)

        # Getting named entities in a text
        for entity in named_entities:
            if "NE" in entity[2]:
                if entity not in ne_list:
                    ne_list.append(entity[0])

        # Returning list of named entities
        return ne_list
