from chatterbot.corpus.utils import read_corpus
import os


os.chdir(os.path.dirname(__file__))

_greetings = read_corpus(os.getcwd() + '/greetings.json')
greetings = _greetings["greetings"]

_conversations = read_corpus(os.getcwd() + '/conversations.json')
conversations = _conversations["conversations"]

