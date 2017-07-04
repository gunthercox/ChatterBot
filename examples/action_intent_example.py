# -*- coding: utf-8 -*-
from chatterbot import ChatBot
import requests

# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

# Create a new instance of a ChatBot
bot = ChatBot(
    'Action or Intent Response Example Bot',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'statement_comparison_function': 'chatterbot.comparisons.jaccard_similarity',
            'response_selection_method': 'chatterbot.response_selection.get_first_response'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Help me!',
            'output_text': 'Ok, here is a link: https://openweathermap.org/current'
        }
    ],
    trainer='chatterbot.trainers.ListTrainer'
)

# Train the chat bot with a few responses
bot.train([
    'Current weather in London',
    'http://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=b1b15e88fa797225412429c1c50c122a1',
    'Have you read the documentation?',
    'No, I have not',
    'This should help get you started: http://chatterbot.rtfd.org/en/latest/quickstart.html'
])

# Get a response from bot
response = bot.get_response('current weather in London?')
# Handle JSON data, get all required data and print them
if 'http' in response.text:
    resp = requests.get(response.text)
    print(resp.json())
