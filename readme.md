![Chatterbot: Machine learning in Python](http://i.imgur.com/b3SCmGT.png)

# ChatterBot

ChatterBot is a machine-learning based conversational dialog engine build in
Python which makes it possible to generate responses based on collections of
known conversations. The language independent design of ChatterBot allows it to
be trained to speak any language.

[![Package Version](https://badge.fury.io/py/ChatterBot.png)](http://badge.fury.io/py/ChatterBot)
[![PyPi](https://pypip.in/download/ChatterBot/badge.svg)](https://pypi.python.org/pypi/ChatterBot)
[![Requirements Status](https://requires.io/github/gunthercox/ChatterBot/requirements.svg?branch=master)](https://requires.io/github/gunthercox/ChatterBot/requirements/?branch=master)
[![Build Status](https://travis-ci.org/gunthercox/ChatterBot.svg?branch=master)](https://travis-ci.org/gunthercox/ChatterBot)
[![Coverage Status](https://img.shields.io/coveralls/gunthercox/ChatterBot.svg)](https://coveralls.io/r/gunthercox/ChatterBot)

An example of typical input would be something like this:

> **user:** Good morning! How are you doing?  
> **bot:**  I am doing very well, thank you for asking.  
> **user:** Your welcome.  
> **bot:** Do you like hats?  

## Installation

This package can be installed from [PyPi](https://pypi.python.org/pypi/ChatterBot) by running:

```
pip install chatterbot
```

### Create a new chat bot  
**Note:** *The `ChatBot` object takes an optional parameter for the bot's name. The default name is 'bot'.*

```
from chatterbot import ChatBot
chatbot = ChatBot("Ron Obvious")
```

### Training
After creating a new chatterbot instance it is also possible to train the bot. Training is a good way to ensure that the bot starts off with knowledge about specific responses. The current training method takes a list of statements that represent a conversation.

**Note:** Training is not required but it is recommended.

```
conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "Your welcome."
]

chatbot.train(conversation)
```

### Get a response

```
response = chatbot.get_response("Good morning!")
print(response)
```

### Change the default log file
**Note:** The default log file is `database.db`.

```
chatbot.database.path = "path/to/file.db"
```

## Other bot types

ChatterBot comes with a selection of useful chat bots built in.

#### Terminal ChatterBot
This is a simple chatterbot that runs in the console. It responds to any user input that is entered.
```
from chatterbot import Terminal
terminal = Terminal()
terminal.begin()
```

### Social ChatterBot
This bot type integrates with various social networking sites to communicate.
```
from chatterbot import SocialBot

TWITTER = {
    "CONSUMER_KEY": "<consumer_key>",
    "CONSUMER_SECRET": "<consumer_secret>"
}

chatbot = SocialBot(twitter=TWITTER)
```

You will need to generate your own keys for using any API. To use this feature with twitter's api you will need to register your application at
[Twitter's developer website](https://dev.twitter.com/apps) to get the token and
secret keys.

### Talk with CleverBot
Want to see what two bots have to say to each other? This allows your ChatterBot to talk to [CleverBot](http://www.cleverbot.com/).
```
from chatterbot import TalkWithCleverbot
talk = TalkWithCleverbot()
talk.begin()
```

## Use Cases

**Using ChatterBot in your app? Let us know!**
- [Salvius (humanoid robot)](https://github.com/gunthercox/salvius)

## History

See release notes for changes https://github.com/gunthercox/ChatterBot/releases
