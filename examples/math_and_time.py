from chatterbot import ChatBot


bot = ChatBot(
    "Math & Time Bot",
    logic_adapters=[
        "chatterbot.adapters.logic.MathematicalEvaluation",
        "chatterbot.adapters.logic.TimeLogicAdapter"
    ],
    input_adapter="chatterbot.adapters.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.adapters.output.OutputFormatAdapter"
)

# Print an example of getting one math based response
response = bot.get_response("What is 4 + 9?")
print(response)

# Print an example of getting one time based response
response = bot.get_response("What time is it?")
print(response)
