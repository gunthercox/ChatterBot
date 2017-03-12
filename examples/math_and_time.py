# -*- coding: utf-8 -*-
from chatterbot import ChatBot


bot = ChatBot(
    "Math & Time Bot",
    logic_adapters=[
        "chatterbot.logic.MathematicalEvaluation",
        "chatterbot.logic.TimeLogicAdapter"
    ],
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter"
)

# Print an example of getting one math based response
response = bot.get_response("What is 4 + 9?")
print(response)

# Print an example of getting one time based response
response = bot.get_response("What time is it?")
print(response)
