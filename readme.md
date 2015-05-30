![Chatterbot: Machine learning in Python](http://i.imgur.com/b3SCmGT.png)

# ChatterBot

ChatterBot is a machine-learning based conversational dialog engine build in
Python which makes it possible to generate responses based on collections of
known conversations. The language independent design of ChatterBot allows it to
be trained to speak any language.

[![Package Version](https://badge.fury.io/py/ChatterBot.png)](http://badge.fury.io/py/ChatterBot)
[![Requirements Status](https://requires.io/github/gunthercox/ChatterBot/requirements.svg?branch=master)](https://requires.io/github/gunthercox/ChatterBot/requirements/?branch=master)
[![Build Status](https://travis-ci.org/gunthercox/ChatterBot.svg?branch=master)](https://travis-ci.org/gunthercox/ChatterBot)
[![Coverage Status](https://img.shields.io/coveralls/gunthercox/ChatterBot.svg)](https://coveralls.io/r/gunthercox/ChatterBot)
[![Code Climate](https://codeclimate.com/github/gunthercox/ChatterBot/badges/gpa.svg)](https://codeclimate.com/github/gunthercox/ChatterBot)

An example of typical input would be something like this:

> **user:** Good morning! How are you doing?  
> **bot:**  I am doing very well, thank you for asking.  
> **user:** You're welcome.  
> **bot:** Do you like hats?  

## How it works

An untrained instance of ChatterBot starts off with no knowledge of how to communicate. Each time a user enters a statement, the library saves the text that they entered and the text that the statement was in response to. As ChatterBot receives more input the number of responses that it can reply and the accuracy of each response in relation to the input statement increase. The program selects the closest matching response by searching for the closest matching known statement that matches the input, it then returns the most likely response to that statement based on how frequently each response is issued by the people the bot communicates with.

## Installation

This package can be installed from [PyPi](https://pypi.python.org/pypi/ChatterBot) by running:

```
pip install chatterbot
```

## Create a new chat bot
```
from chatterbot import ChatBot
chatbot = ChatBot("Ron Obvious")
```
**Note:** *The `ChatBot` requires that a name is specified for the bot.

## Training
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
    "You're welcome."
]

chatbot.train(conversation)
```

## Get a response

```
response = chatbot.get_response("Good morning!")
print(response)
```

## Logging

Your ChatterBot will learn based on each new input statement it recieves.
If you do not want your bot to learn, set `logging=False` when initializing the
bot.

```
chatbot = ChatBot("Johnny Five", logging=False)
```

# Adapters

ChatterBot uses adapters to handle three types of operations. All adapters for
ChatterBot fall into one of three categories: **storage**, **io**, and **logic**.

By default, ChatterBot uses the `JsonDatabaseAdapter` adapter for storage,
the `EngramAdapter` for logic, and the `TerminalAdapter` for IO.

Each adapter can be set by passing in the dot-notated import path to the constructor.

```
bot = ChatBot("My ChatterBot",
    storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
    logic_adapter="chatterbot.adapters.logic.EngramAdapter",
    io_adapter="chatterbot.adapters.io.TerminalAdapter",
    database="../database.db")
```

## Storage adapters

Storage adapters allow ChatterBot to connect to connect to any type of storage
backend.

### `JsonDatabaseAdapter`

```
"chatterbot.adapters.storage.JsonDatabaseAdapter"
```

The JSON Database adapter requires an additional parameter (`database`) to be
passed to the ChatterBot constructor. This storage adapter uses a local file
database so this parameter is needed to specify the location of the file.

## IO adapters

IO adapters allow ChatterBot to communicate through various interfaces. The
default io adapter uses the terminal to communicate with the user.

### `TerminalAdapter`

```
"chatterbot.adapters.io.TerminalAdapter"
```

The terminal adapter allows the ChatterBot to communicate with you through your
terminal.

## Logic adapters

Logic adapters determine how ChatterBot selects responces to input statements.

### `EngramAdapter`

```
"chatterbot.adapters.logic.EngramAdapter"
```

The engram adapter selects a response based on the closest know match to a
given statement.

# Examples

For examples, see the [examples](https://github.com/gunthercox/ChatterBot/tree/master/examples)
directory in this project's repository.

# Testing

ChatterBot's built in tests can be run using nose.  
See the [nose documentation](https://nose.readthedocs.org/en/latest/) for more information.

# Use Cases

**Using ChatterBot in your app? Let us know!**

|[Salvius the Robot](https://github.com/gunthercox/salvius)|A humanoid robot.|
|---|---|
|[Zuluhotel](http://zuluhotel3.com)|A mmorpg shard emulation game.|

# History

See release notes for changes https://github.com/gunthercox/ChatterBot/releases
