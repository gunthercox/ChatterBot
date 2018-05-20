# -*- coding: utf-8 -*-
from chatterbot import ChatBot


bot = ChatBot(
    "Unit Converter",
    logic_adapters=[
        "chatterbot.logic.UnitConversion",
    ],
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter"
)

questions = ['How many meters are in a kilometer?',
             'How many meters are in one inch?',
             '0 celsius to fahrenheit',
             'one hour is how many minutes ?']

# Prints the convertion given the specific question
for q in questions:
    response = bot.get_response(q)
    print(q + " -  Response: " + response.text)
