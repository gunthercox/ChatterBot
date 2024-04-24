![ChatterBot: Machine learning in Python](https://i.imgur.com/b3SCmGT.png)
<h4 align="center">
    <p>
        <a href="https://github.com/WThirteen/ChatterBot/edit/master/README_zh.md">中文</a> |
        <a href="https://github.com/WThirteen/ChatterBot/edit/master/README.md">English</a>
    <p>
</h4>

# ChatterBot

ChatterBot 是一个基于机器学习的对话对话引擎内置Python，可以基于已知对话。  
ChatterBot 的语言独立设计允许它接受任何语言的培训。

[![Package Version](https://img.shields.io/pypi/v/chatterbot.svg)](https://pypi.python.org/pypi/chatterbot/)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Django 2.0](https://img.shields.io/badge/Django-2.0-blue.svg)](https://docs.djangoproject.com/en/2.1/releases/2.0/)
[![Requirements Status](https://requires.io/github/gunthercox/ChatterBot/requirements.svg?branch=master)](https://requires.io/github/gunthercox/ChatterBot/requirements/?branch=master)
[![Build Status](https://travis-ci.org/gunthercox/ChatterBot.svg?branch=master)](https://travis-ci.org/gunthercox/ChatterBot)
[![Documentation Status](https://readthedocs.org/projects/chatterbot/badge/?version=stable)](http://chatterbot.readthedocs.io/en/stable/?badge=stable)
[![Coverage Status](https://img.shields.io/coveralls/gunthercox/ChatterBot.svg)](https://coveralls.io/r/gunthercox/ChatterBot)
[![Code Climate](https://codeclimate.com/github/gunthercox/ChatterBot/badges/gpa.svg)](https://codeclimate.com/github/gunthercox/ChatterBot)
[![Join the chat at https://gitter.im/chatterbot/Lobby](https://badges.gitter.im/chatterbot/Lobby.svg)](https://gitter.im/chatterbot/Lobby?utm_source=badge&utm_medium=badge&utm_content=badge)

典型输入的示例如下：  

> **user:** Good morning! How are you doing?  
> **bot:**  I am doing very well, thank you for asking.  
> **user:** You're welcome.  
> **bot:** Do you like hats?  

## 运作方式

未经训练的 ChatterBot 实例开始时不知道如何沟通。每次用户输入语句时，库都会保存他们输入的文本以及语句响应的文本。随着 ChatterBot 接收到的输入越多，它可以回复的响应数量以及每个响应与输入语句相关的准确性也会增加。该程序通过搜索与输入匹配的最接近的匹配已知语句来选择最接近的匹配响应，然后根据机器人与之通信的人员发出每个响应的频率返回对该语句的最可能的响应。

## 安装

这个包可以从 [PyPi](https://pypi.python.org/pypi/ChatterBot) 通过运行：
```
pip install chatterbot
```

## 基本用法

```
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot('Ron Obvious')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english")

# Get a response to an input statement
chatbot.get_response("Hello, how are you today?")
```

# 训练数据

ChatterBot 带有一个数据实用程序模块，可用于训练聊天机器人。
目前，该模块中有十几种语言的训练数据。
贡献额外的训练数据或训练数据
在其他语言中将不胜感激。查看数据文件
在 [chatterbot-corpus](https://github.com/gunthercox/chatterbot-corpus) 中
如果您有兴趣做出贡献，请打包。

```
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train based on the english corpus
trainer.train("chatterbot.corpus.english")

# Train based on english greetings corpus
trainer.train("chatterbot.corpus.english.greetings")

# Train based on the english conversations corpus
trainer.train("chatterbot.corpus.english.conversations")
```

** 欢迎语料库投稿！请提出拉取请求。**

# [文档](https://chatterbot.readthedocs.io/)

查看 [文档](https://chatterbot.readthedocs.io/)
对于 ChatterBot，请阅读文档。

要使用 [Sphinx](http://www.sphinx-doc.org/) 自行构建文档，请运行：

```
sphinx-build -b html docs/ build/
```

# 示例

有关示例，请参阅 [examples](https://github.com/gunthercox/ChatterBot/tree/master/examples)
目录。

还有一个示例 [使用 ChatterBot 的 Django 项目](https://github.com/gunthercox/ChatterBot/tree/master/examples)，以及一个示例 [使用 ChatterBot 的 Flask 项目](https://github.com/chamkank/flask-chatterbot)。

# 历史

有关更改 https://github.com/gunthercox/ChatterBot/releases，请参阅发行说明

# Development pattern for contributors

1. [Create a fork](https://help.github.com/articles/fork-a-repo/) of
   the [main ChatterBot repository](https://github.com/gunthercox/ChatterBot) on GitHub.
2. Make your changes in a branch named something different from `master`, e.g. create
   a new branch `my-pull-request`.
3. [Create a pull request](https://help.github.com/articles/creating-a-pull-request/).
4. Please follow the [Python style guide for PEP-8](https://www.python.org/dev/peps/pep-0008/).
5. Use the projects [built-in automated testing](https://chatterbot.readthedocs.io/en/latest/testing.html).
   to help make sure that your contribution is free from errors.

# 贡献者开发模式

1. [创建分叉](https://help.github.com/articles/fork-a-repo/) 的
   GitHub 上的 [主 ChatterBot 存储库](https://github.com/gunthercox/ChatterBot)。
2. 在名为“master”的分支中进行更改，例如 create
   一个新分支“my-pull-request”。
3. [创建拉取请求](https://help.github.com/articles/creating-a-pull-request/)。
4. 请遵循 [PEP-8 的 Python 样式指南](https://www.python.org/dev/peps/pep-0008/)。
5. 使用项目[内置自动化测试](https://chatterbot.readthedocs.io/en/latest/testing.html)。
   以帮助确保您的贡献没有错误。
   
# 许可证

ChatterBot 根据 [BSD 3 条款许可证](https://opensource.org/licenses/BSD-3-Clause) 获得许可。
