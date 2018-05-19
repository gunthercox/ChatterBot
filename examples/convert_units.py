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

# Prints the convertion from one kilometer to meters
response = bot.get_response('How many meters are in a kilometer?')
print(response.text)

# Prints the convertion from one inch to meters
response = bot.get_response('How many meters are in one inch?')
print(response.text)
