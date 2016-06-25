![Aprendizaje automático en Python: Chatterbot](http://i.imgur.com/b3SCmGT.png)

# Chatterbot

Chatterbot es un robot machine-learning de diálogo conversacional basado en aprendizaje automático en Python que hace posible la generación de respuestas basado en las colecciones de conversaciones conocidas. Su diseño independiente del idioma de Chatterbot permite que sea entrenado para hablar cualquier idioma.

*[Read in English](readme.md)*
*[Leia em Português](readme.pt.md)*
*[Leer en español](readme-es.md)*

[![Versión del paquete](https://img.shields.io/pypi/v/chatterbot.svg)](https://pypi.python.org/pypi/chatterbot/) [![requisitos Estado](https://requires.io/github/gunthercox/ChatterBot/requirements.svg?branch=master)](https://requires.io/github/gunthercox/ChatterBot/requirements/?branch=master) [![Estado de creación](https://travis-ci.org/gunthercox/ChatterBot.svg?branch=master)](https://travis-ci.org/gunthercox/ChatterBot) [![Estado de la documentación](https://readthedocs.org/projects/chatterbot/badge/?version=latest)](http://chatterbot.readthedocs.io/en/latest/?badge=latest) [![Estado de la cobertura](https://img.shields.io/coveralls/gunthercox/ChatterBot.svg)](https://coveralls.io/r/gunthercox/ChatterBot) [![código climático](https://codeclimate.com/github/gunthercox/ChatterBot/badges/gpa.svg)](https://codeclimate.com/github/gunthercox/ChatterBot)

Un ejemplo de conversación típica sería algo como esto:

> **usuario:** Buenos días! ¿Como estas?
> **bot:** Me está yendo muy bien, gracias por preguntar.
> **usuario:** No hay de qué.
> **bot:** ¿Te gustan los sombreros?

## Cómo funciona

Una instancia de Chatterbot sin entrenamiento comienza con ningún conocimiento de cómo comunicarse. Cada vez que un usuario ingresa algo, la biblioteca guarda el texto que ingreso y el texto a lo que respondia. Cuando Chatterbot recibe más texto, el número de respuestas que puede responder y la exactitud de cada respuesta aumenta en relación con las sentencias de entrada. El programa selecciona la respuestas más parecida mediante la búsqueda de la declaración conocida más parecida que coincide con la entrada, después, devuelve la respuesta más probable a esta afirmación basada en la frecuencia con que cada respuesta es emitida por la persona con el bot que se comunica.

## Instalación

Este paquete se puede instalar desde [PyPi](https://pypi.python.org/pypi/ChatterBot) ejecutando:

```
pip install chatterbot

```

## Uso básico

```
from chatterbot import ChatBot
from chatterbot.training.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot("Ron Obvious")
chatbot.set_trainer(ChatterBotCorpusTrainer)

# Enseñar de acuerdo al corpus español
chatbot.train("chatterbot.corpus.spanish")

# Obtener una respuesta a una sentencia de entrada
chatbot.get_response("Hola, ¿Que tal estas hoy?")

```

# Datos de entrenamiento

Chatterbot viene con un módulo de utilidad de datos que se puede utilizar para entrenar a los robots de chat. Por el momento hay tres idiomas para el entrenamiento en este modulo, inglés portugués y español. Las contribuciones de datos de entrenamiento adicional o datos de entrenamiento en otros idiomas serán gratamente bienvenidas. Echa un vistazo a los archivos de datos en el directorio [chatterbot/corpus](https://github.com/gunthercox/ChatterBot/tree/master/chatterbot/corpus) si estás interesado en contribuir.

```
# Entrenamiento basado en el corpus español
chatbot.train("chatterbot.corpus.spanish")

# Entrenamiento basado en el corpus español de saludos
chatbot.train("chatterbot.corpus.spanish.greetings")

# Entrenamiento basado en el corpus español de conversaciones
chatbot.train("chatterbot.corpus.spanish.conversations")

```

**Las contribuciones de Corpus son bienvenidas! Por favor haga un pull request.**

# [Documentación](http://chatterbot.readthedocs.io/) (Sin Traducir)

Ver la [documentación](http://chatterbot.readthedocs.io/) para chatterbot en Leer los Docs.

# Ejemplos

Para ejemplos, véase el directorio [ejemplos](https://github.com/gunthercox/ChatterBot/tree/master/examples) en el repositorio de este proyecto.

También hay un ejemplo [de proyecto de Django usando chatterbot](https://github.com/gunthercox/django_chatterbot) .

**¿Ha creado algo guay usando Chatterbot?**

Por favor, añada su creación a la [lista de proyectos](https://github.com/gunthercox/ChatterBot/wiki/ChatterBot-Showcase) que utilizan Chatterbot en el wiki.

# Pruebas

Chatterbot se puede "testear" usando nose.

```
nosetests

```

Consulte la [documentación de nose](https://nose.readthedocs.org/en/latest/) para obtener más información.

# Historia

Ver notas de cambios para la versión [https://github.com/gunthercox/ChatterBot/releases](https://github.com/gunthercox/ChatterBot/releases)