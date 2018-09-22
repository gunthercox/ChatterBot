from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging


'''
This is an example showing how to train a chat bot using the
ChatterBot Corpus of conversation dialog.
'''

# Enable info level logging
logging.basicConfig(level=logging.INFO)

chatbot = ChatBot('Example Bot')

# Start by training our bot with the ChatterBot corpus data
trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train(
    'chatterbot.corpus.english'
)

# Now let's get a response to a greeting
response = chatbot.get_response('How are you doing today?')
print(response)
