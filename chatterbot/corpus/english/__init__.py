from chatterbot.corpus.utils import read_corpus
import os, sys


current_directory = os.path.dirname(__file__)

_greetings = read_corpus(current_directory + '/greetings.json')
_conversations = read_corpus(current_directory + '/conversations.json')

setattr(
    sys.modules[__name__],
    'greetings', _greetings['greetings']
)

setattr(
    sys.modules[__name__],
    'conversations', _conversations['conversations']
)

modules = [_greetings, _conversations]

