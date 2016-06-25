![Chatterbot: Machine learning in Python](http://i.imgur.com/b3SCmGT.png)

# ChatterBot

ChatterBot é uma engine baseada em aprendizado de máquina através de diálogos
de conversação construído em Python o que possibilita a geração de respostas 
baseada em coleções de conversas conhecidas. A arquitetura do ChatterBot
é independente da língua, desta forma é possível treiná-lo em qualquer língua.

*[Read in English](readme.md)*
*[Leia em Português](readme.pt.md)*
*[Leer en español](readme-es.md)*

[![Package Version](https://img.shields.io/pypi/v/chatterbot.svg)](https://pypi.python.org/pypi/chatterbot/)
[![Requirements Status](https://requires.io/github/gunthercox/ChatterBot/requirements.svg?branch=master)](https://requires.io/github/gunthercox/ChatterBot/requirements/?branch=master)
[![Build Status](https://travis-ci.org/gunthercox/ChatterBot.svg?branch=master)](https://travis-ci.org/gunthercox/ChatterBot)
[![Coverage Status](https://img.shields.io/coveralls/gunthercox/ChatterBot.svg)](https://coveralls.io/r/gunthercox/ChatterBot)
[![Code Climate](https://codeclimate.com/github/gunthercox/ChatterBot/badges/gpa.svg)](https://codeclimate.com/github/gunthercox/ChatterBot)

Um exemplo típico de entrada, será algo parecido com isso:

> **Usuário:** Bom dia, como você esta?  
> **Robô:**  Estou muito bem, obrigado por perguntar.  
> **Usuário:** De nada.  
> **Robô:** Você gosta de chapéus?  

## Como funciona

Uma instância não treinada do ChatterBot começão sem conhecimento de como se comunicar. Cada vez que o usuário entra com uma afirmação, a bibliote salve o texto que foi inserido e o texto em que a afirmação foi respondida. Conforme o ChatterBot recebe mais entradas o número de respostas que ele pode responder e a precisão de suas respostas em relação a afirmação de entrada cresce. O programa seleciona a resposta mais precisa procurando pela resposta mais próxima que combina com a afirmação de entrada, ele então retorna a resposta mais provável para a afirmação baseada na frequência que esta resposta é emitida pelao usuário que esta se comunicando com o robô.

## Instalação

Este pacote pode ser instalado através de [PyPi](https://pypi.python.org/pypi/ChatterBot) execuntando o seguinte comando:

```
pip install chatterbot
```

## Uso básico

```
from chatterbot import ChatBot
chatbot = ChatBot("Ron Obvious")

# Treino baseado no corpus em português
chatbot.train("chatterbot.corpus.Portuguese")

# Obtenha uma resposta para uma pergunta
chatbot.get_response("Olá, como você esta hoje?")
```

# Treinando os dados

ChatterBot vem com um módulo utilitário de dados que pode ser usado para treinar os robôs de chat.
Neste momento existem dados de treinamento em Inglês, Espanhol e Português neste módulo. Contribuições de dados de treinamento adicionais
ou dados de treinamento em outras linguagem será muito bem vinda. Dê uma olhada nos arquivos de dados em [chatterbot/corpus](https://github.com/gunthercox/ChatterBot/tree/master/chatterbot/corpus)
se você estiver interesse em contribuir.

```
# Treino baseado no corpus em Portugues 
chatbot.train("chatterbot.corpus.Portuguese")

# Treino baseado no corpus de saudações em Português
chatbot.train("chatterbot.corpus.Portuguese.greetings_pt-BT")

# Train based on the english conversations corpus
# Treino baseado no corpus de conversação em Português
chatbot.train("chatterbot.corpus.Portuguese.conversations_pt-BR")
```

**Corpus contributions are welcome! Please make a pull request.**
**Contribuições ao Corpus são bem-vindas! Por favor faça uma pull request.** 

# Documentação

Veja a [documentação](https://github.com/gunthercox/ChatterBot/wiki/)
para usar o ChatterBot na wiki do projeto.

# Exemplos

Para consultar exemplos, veja o diretório de [exemplos](https://github.com/gunthercox/ChatterBot/tree/master/examples) no repositório
deste projeto.

There is also an example [Django project using ChatterBot](https://github.com/gunthercox/django_chatterbot).
Também existe exemplos em [Projeto Django usando o ChatterBot](https://github.com/gunthercox/django_chatterbot).

Criou algo legal usando o ChatterBot?
Por favor adicione a sua criação na [lista de projetos](https://github.com/gunthercox/ChatterBot/wiki/ChatterBot-Showcase) usando o ChatterBot na Wiki.

# Testando

Os testes nativos do ChatterBot podem ser executados usando nose.

Veja a [documentação do nose](https://nose.readthedocs.org/en/latest/) para mais informações.

# História

Veja as notas de lançamento de mudanças  https://github.com/gunthercox/ChatterBot/releases
