from nltk.corpus import wordnet


class Wordnet(object):
    """
    A custom-implementation of Wordnet. Not many
    features are supported at the moment, only:
    1) synsets: Returns the synsets of a token
    """

    def __init__(self):
        from nltk.data import find
        from nltk import download
        import os

        # Download the wordnet data only if it is not already downloaded
        wordnet_path = None
        if os.name == 'nt':
            wordnet_path = os.path.join(
                os.getenv('APPDATA'), 'nltk_data', 'corpora', 'wordnet.zip'
            )
        else:
            wordnet_path = os.path.join(
                os.path.expanduser('~'), 'nltk_data', 'corpora', 'wordnet.zip'
            )
        try:
            if not os.path.isfile(wordnet_path):
                find('wordnet.zip')
        except LookupError:
            download('wordnet')

    def synsets(self, token):
        """
        Takes a token and returns the synsets for
        it.
        """
        return wordnet.synsets(token)
