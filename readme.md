# ChatBot [![Build Status](https://travis-ci.org/gunthercox/ChatBot.svg?branch=master)](https://travis-ci.org/gunthercox/ChatBot)

This is a ChatBot program that takes input and returns a response based on known conversations.

## A general warning

This program is capable of retrieving conversation data from various social networks
in order to provide more accurate replies to input text. Because of this,
the chat bot can provide rather profane response at random. I have plans to address
this issue, however they are not yet implemented.

## Useage

Create a new chat bot
```
from engram import Engram
chatbot = Engram()
```

Getting a response
```
response = chatbot.engram("Good morning!")
print(response)
```

Terminal mode (User and chat bot)
```
chatbot.terminal(False)
```

Have the chat bot talk with CleverBot
```
chatbot.talk_with_cleverbot(True)
```

## Requirements

To install required packages for this project run the command:
```sudo pip install -r requirements.md```

## Notes

This program is not designed to be an open source version of CleverBot.
Although this **ChatBot** returns responces, the code here handles communication
much differently then [CleverBot](http://www.cleverbot.com) does.
