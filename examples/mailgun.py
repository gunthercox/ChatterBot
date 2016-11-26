# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from settings import MAILGUN

'''
To use this example, create a new file called settings.py.
In settings.py define the following:

MAILGUN = {
    "CONSUMER_KEY": "my-mailgun-api-key",
    "API_ENDPOINT": "https://api.mailgun.net/v3/my-domain.com/messages"
}
'''

# Change these to match your own email configuration
FROM_EMAIL = "mailgun@salvius.org"
RECIPIENTS = ["gunthercx@gmail.com"]

bot = ChatBot(
    "Mailgun Example Bot",
    mailgun_from_address=FROM_EMAIL,
    mailgun_api_key=MAILGUN["CONSUMER_KEY"],
    mailgun_api_endpoint=MAILGUN["API_ENDPOINT"],
    mailgun_recipients=RECIPIENTS,
    input_adapter="chatterbot.input.Mailgun",
    output_adapter="chatterbot.output.Mailgun",
    storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
    database="../database.db"
)

# Send an example email to the address provided
response = bot.get_response("How are you?")
print("Check your inbox at ", RECIPIENTS)
