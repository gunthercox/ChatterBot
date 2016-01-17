from chatterbot import ChatBot


bot = ChatBot(
    "Math & Time Bot",
    logic_adapters=[
        "chatterbot.adapters.logic.EvaluateMathematically",
        "chatterbot.adapters.logic.TimeLogicAdapter"
    ],
    io_adapter="chatterbot.adapters.io.NoOutputAdapter"
)

# Print an example of getting one math based response
response = bot.get_response("What is 4 + 9?")
print(response)

# Print an example of getting one time based response
response = bot.get_response("What time is it?")
print(response)
