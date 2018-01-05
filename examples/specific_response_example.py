# -*- coding: utf-8 -*-
from chatterbot import ChatBot


# Create a new instance of a ChatBot
bot = ChatBot(
    'Exact Response Example Bot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Help me!',
            'output_text': 'Ok, here is a link: http://chatterbot.rtfd.org'
        }
    ],
    trainer='chatterbot.trainers.ListTrainer'
)

# Get a response given the specific input
response = bot.get_response('Help me!')
print(response)
