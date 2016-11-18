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
bot = ChatBot('Feedback Learning Bot',
    storage_adapter='chatterbot.adapters.storage.JsonFileStorageAdapter',
    logic_adapters=[
        'chatterbot.adapters.logic.ClosestMatchAdapter'
    ],
    input_adapter='chatterbot.adapters.input.TerminalAdapter',
    output_adapter='chatterbot.adapters.output.TerminalAdapter'
)

def get_feedback():
    from chatterbot.utils.read_input import input_function

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
        statement, response, confidence = bot.generate_response(input_statement)

        print('\n Is "{}" this a coherent response to "{}"? \n'.format(response, input_statement))

        if get_feedback():
            bot.learn_response(response)

        bot.output.process_response(response, confidence)

        # Update the conversation history for the bot
        # It is important that this happens last, after the learning step
        bot.recent_statements.append(
            (statement, response, )
        )

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
