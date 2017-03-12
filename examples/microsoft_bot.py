# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from settings import Microsoft

'''
See the Microsoft DirectLine api documentation for how to get a user access token.
https://docs.botframework.com/en-us/restapi/directline/
'''

chatbot = ChatBot(
    'MicrosoftBot',
    directline_host = Microsoft['directline_host'],
    direct_line_token_or_secret = Microsoft['direct_line_token_or_secret'],
    conversation_id = Microsoft['conversation_id'],
    input_adapter='chatterbot.input.Microsoft',
    output_adapter='chatterbot.output.Microsoft',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

chatbot.train('chatterbot.corpus.english')

# The following loop will execute each time the user enters input
while True:
    try:
        response = chatbot.get_response(None)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
