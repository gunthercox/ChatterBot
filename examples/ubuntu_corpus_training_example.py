"""
This example shows how to train a chat bot using the
Ubuntu Corpus of conversation dialog.
"""
import logging
from chatterbot import ChatBot
from chatterbot.trainers import UbuntuCorpusTrainer

# Enable info level logging
logging.basicConfig(level=logging.INFO)

chatbot = ChatBot('Example Bot')

trainer = UbuntuCorpusTrainer(chatbot)

# Start by training our bot with the Ubuntu corpus data
trainer.train()

# Now let's get a response to a greeting
response = chatbot.get_response('How are you doing today?')
print(response)
