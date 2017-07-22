# -*- coding: utf-8 -*-
from chatterbot import ChatBot

# Create a new chat bot named Charlie
chatbot = ChatBot(
    'Charlie',
    trainer='chatterbot.trainers.ListTrainer'
)

chatbot.train([
    "Hi, can I help you?",
    "Sure, I'd to book a flight to Iceland.",
    "Your flight has been booked."
])

# Get a response to the input text 'How are you?'
response = chatbot.get_response('I would like to book a flight.')

print(response)
