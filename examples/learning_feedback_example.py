# -*- coding: utf-8 -*-
from chatterbot import ChatBot

"""
This example shows how to create a chat bot that
will learn responses based on an additional feedback
element from the user.
"""

# Uncomment the following line to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

CONVERSATION = 'example_feedback_conversation'

# Create a new instance of a ChatBot
bot = ChatBot(
    'Feedback Learning Bot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ],
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter'
)


def get_feedback():

    text = input()

    if 'yes' in text.lower():
        return True
    elif 'no' in text.lower():
        return False
    else:
        print('Please type either "Yes" or "No"')
        return get_feedback()


print('Type something to begin...')

# The following loop will execute each time the user enters input
while True:
    try:
        input_statement = bot.input.process_input_statement()
        statement, response = bot.generate_response(
            input_statement,
            CONVERSATION
        )
        print('\n Is "{}" this a coherent response to "{}"? \n'.format(response, input_statement))

        if get_feedback():
            bot.learn_response(CONVERSATION, response, input_statement)

        bot.output.process_response(response)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
