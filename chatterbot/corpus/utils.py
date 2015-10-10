import json

def read_corpus(file_name):
    """
    Read and return the data from a corpus json file.
    """
    with open(file_name) as data_file:    
        data = json.load(data_file)
    return data

def load_corpus(corpus_path):
    """
    Return the data contained within a specified corpus.
    """
    from chatterbot.utils.module_loading import import_module
    from types import ModuleType

    corpus = import_module(corpus_path)

    if isinstance(corpus, ModuleType):
        corpora = []
        for module in corpus.modules:
            for key in list(module.keys()):
                corpora.append(module[key])
        return corpora

    return [corpus]

