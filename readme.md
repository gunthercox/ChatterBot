![Chatterbot: Machine learning in Python](http://i.imgur.com/b3SCmGT.png)

# ChatterBot

ChatterBot is a machine-learning based conversational dialog engine build in
Python which makes it possible to generate responses based on collections of
known conversations. The language independent design of ChatterBot allows it to
be trained to speak any language.

[![Package Version](https://badge.fury.io/py/ChatterBot.png)](http://badge.fury.io/py/ChatterBot)
[![Build Status](https://travis-ci.org/gunthercox/ChatterBot.svg?branch=master)](https://travis-ci.org/gunthercox/ChatterBot)
[![PyPi](https://pypip.in/download/ChatterBot/badge.svg)](https://pypi.python.org/pypi/ChatterBot)
[![Coverage Status](https://img.shields.io/coveralls/gunthercox/ChatterBot.svg)](https://coveralls.io/r/gunthercox/ChatterBot)

An example of typical input would be something like this:

> **user:** Good morning! How are you doing?  
> **bot:**  I am doing very well, thank you for asking.  
> **user:** Your welcome.  
> **bot:** Do you like hats?  

## Installation

This package can be installed using

```
pip install chatterbot
```

## Usage

Create a new chat bot  
**Note:** *This object takes an optional parameter for the bot's name.*

```
from chatterbot import ChatBot
chatbot = ChatBot("Ron Obvious")
```

After creating a new chatterbot instance it is also possible to train the bot.
Training is a good way to ensure that the bot starts off with knowledge about
specific responses.

**Note** Training is recommended, but not required. The bot will begin learning
as soon as it starts receiving input.

```
conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm great.",
    "That is good to hear",
    "Thank you.",
    "Your welcome.",
    "Sure, any time.",
    "Yeah",
    "Can I help you with anything?"
]

chatbot.train(conversation)
```

Getting a response to input text

```
response = chatbot.get_response("Good morning!")
print(response)
```

Specify a default location for conversation log files  
**Note:** The default log location is `./database.db`.

```
chatbot.database.path = "path/to/file.db"
```

**Terminal mode (User and chat bot)**

```
from chatterbot import Terminal
terminal = Terminal()
terminal.begin()
```

**Have the chat bot talk with CleverBot**

```
from chatterbot import TalkWithCleverbot
talk = TalkWithCleverbot()
talk.begin()
```

**Social mode (Have the bot respond to users on social media sites)**

```
from chatterbot import SocialBot

TWITTER = {
    "CONSUMER_KEY": "<consumer_key>",
    "CONSUMER_SECRET": "<consumer_secret>"
}

chatbot = SocialBot(twitter=TWITTER)
```

You will need to generate your own keys for using any API. To use this feature
you will need to register your application at
[Twitter's developer website](https://dev.twitter.com/apps) to get the token and
secret keys.

## Use Cases

**Using ChatterBot in your app? Let us know!**
- [Salvius (humanoid robot)](https://github.com/gunthercox/salvius)

## Notes

Sample conversations for training the chat bot can be downloaded
from https://gist.github.com/gunthercox/6bde8279615b9b638f71
