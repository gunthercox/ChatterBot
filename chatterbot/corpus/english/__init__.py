from chatterbot.corpus.utils import read_corpus
import os, sys


os.chdir(os.path.dirname(__file__))

_greetings = read_corpus(os.getcwd() + '/greetings.json')
_conversations = read_corpus(os.getcwd() + '/conversations.json')

setattr(
    sys.modules[__name__],
    'greetings', _greetings['greetings']
)

setattr(
    sys.modules[__name__],
    'conversations', _conversations['conversations']
)

modules = [_greetings, _conversations]

