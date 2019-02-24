from pickle import dump, load
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
from nltk.tokenize import _treebank_word_tokenizer
from chatterbot.corpus import load_corpus, list_corpus_files
from chatterbot import languages


def get_sentence_tokenizer(language):
    """
    Return the sentence tokenizer callable.
    """

    pickle_path = 'sentence_tokenizer.pickle'

    try:
        input_file = open(pickle_path, 'rb')
        sentence_tokenizer = load(input_file)
        input_file.close()
    except FileNotFoundError:

        data_file_paths = []

        sentences = []

        try:
            # Get the paths to each file the bot will be trained with
            corpus_files = list_corpus_files('chatterbot.corpus.{language}'.format(
                language=language.ENGLISH_NAME.lower()
            ))
        except LookupError:
            # Fall back to English sentence splitting rules if a language is not supported
            corpus_files = list_corpus_files('chatterbot.corpus.{language}'.format(
                language=languages.ENG.ENGLISH_NAME.lower()
            ))

        data_file_paths.extend(corpus_files)

        for corpus, _categories, _file_path in load_corpus(*data_file_paths):
            for conversation in corpus:
                for text in conversation:
                    sentences.append(text.upper())
                    sentences.append(text.lower())

        trainer = PunktTrainer()
        trainer.INCLUDE_ALL_COLLOCS = True
        trainer.train('\n'.join(sentences))

        sentence_tokenizer = PunktSentenceTokenizer(trainer.get_params())

        # Pickle the sentence tokenizer for future use
        output_file = open(pickle_path, 'wb')
        dump(sentence_tokenizer, output_file, -1)
        output_file.close()

    return sentence_tokenizer


def get_word_tokenizer(language):
    """
    Return the word tokenizer callable.
    """
    return _treebank_word_tokenizer
