# -*- coding: utf-8 -*-
from chatterbot import ChatBot
import logging

"""
This example shows how to create a chat bot that
will learn responses based on an additional feedback
element from the user.
"""

# Uncomment the following line to enable verbose logging
# logging.basicConfig(level=logging.INFO)

# Create a new instance of a ChatBot
bot = ChatBot(
    'Feedback Learning Bot',
    storage_adapter='chatterbot.storage.JsonFileStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ],
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter'
)

DEFAULT_SESSION_ID = bot.default_session.id


def get_feedback():
    from chatterbot.utils import input_function

    text = input_function()

    if 'Yes' in text:
        return True
    elif 'No' in text:
        return False
    else:
        print('Please type either "Yes" or "No"')
        return get_feedback()


print('Type something to begin...')

# The following loop will execute each time the user enters input
while True:
    try:
        input_statement = bot.input.process_input_statement()
        statement, response = bot.generate_response(input_statement, DEFAULT_SESSION_ID)

        print('\n Is "{}" this a coherent response to "{}"? \n'.format(response, input_statement))

        if get_feedback():
            bot.learn_response(response,input_statement)

        bot.output.process_response(response)

        # Update the conversation history for the bot
        # It is important that this happens last, after the learning step
        bot.conversation_sessions.update(
            bot.default_session.id_string,
            (statement, response, )
        )

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
