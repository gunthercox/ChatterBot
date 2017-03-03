![Chatterbot: Machine learning in Python](http://i.imgur.com/b3SCmGT.png)

# ChatterBot

ChatterBot è un motore di conversazione basato su machine learning costruito 
con Python che rende possibile generare risposte automatiche basate su collezioni
di conversazioni conociute. Un'architettura indipendente dalla lingua scelta
permette a ChatterBot di essere allenato per parlare qualsiasi lingua.

*[Read in English](readme.md)*
*[Leia em Português](readme.pt.md)*
*[Leer en español](readme.es.md)*
*[Leggi in Italiano](readme.it.md)*

[![Package Version](https://img.shields.io/pypi/v/chatterbot.svg)](https://pypi.python.org/pypi/chatterbot/)
[![Requirements Status](https://requires.io/github/gunthercox/ChatterBot/requirements.svg?branch=master)](https://requires.io/github/gunthercox/ChatterBot/requirements/?branch=master)
[![Build Status](https://travis-ci.org/gunthercox/ChatterBot.svg?branch=master)](https://travis-ci.org/gunthercox/ChatterBot)
[![Documentation Status](https://readthedocs.org/projects/chatterbot/badge/?version=stable)](http://chatterbot.readthedocs.io/en/stable/?badge=stable)
[![Coverage Status](https://img.shields.io/coveralls/gunthercox/ChatterBot.svg)](https://coveralls.io/r/gunthercox/ChatterBot)
[![Code Climate](https://codeclimate.com/github/gunthercox/ChatterBot/badges/gpa.svg)](https://codeclimate.com/github/gunthercox/ChatterBot)
[![Join the chat at https://gitter.im/chatter_bot/Lobby](https://badges.gitter.im/chatter_bot/Lobby.svg)](https://gitter.im/chatter_bot/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Un esempio di conversazione tipica è il seguente:

> **utente:** Buongiorno! Come stai?  
> **bot:**  Benissimo, grazie per la domanda.  
> **user:** Prego.  
> **bot:** Ti piacciono i cappelli?  

## Come funziona

Un'istanza non allenata di ChatterBot nasce senza alcuna conoscenza di come comunicare. Ogni volta che l'utente inserisce una frase, la libreria salva il testo inserito e il rispettivo testo di risposta. Più aumenta il numero di frasi, maggiore diventano accuratezza e numero di frasi di risposta in relazione all'input inserito. Il programma seleziona la risposta ottimale cercando fra le domande conosciute la più simile a quella fornita, restituendo la risposta più probabile in base al numero di risposte fornite dagli utenti nelle conversazioni avute fino a quel momento.

## Installazione

Il pacchetto può essere installato da [PyPi](https://pypi.python.org/pypi/ChatterBot) usando:

```
pip install chatterbot
```

## Utilizzo di base

```
from chatterbot import ChatBot

chatbot = ChatBot(
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

# Allena il bot con il dizionario inglese
chatbot.train("chatterbot.corpus.english")

# Ottieni una risposta ad una domanda
chatbot.get_response("Hello, how are you today?")
```

# Dati di training

Chatterbot include una utility che può essere usata per allenare i chat bots.
Al momento, tre lingue sono supportate, e sono l'inglese, lo spagnolo e il portoghese. 
Contributi addizionali o contributi in altre lingue sono sempre i benvenuti. A questo fine, controllate la cartella
[chatterbot/corpus](https://github.com/gunthercox/ChatterBot/tree/master/chatterbot/corpus)
se siete interessati a contribuire al progetto.

```
# Allena il bot con il dizionario inglese
chatbot.train("chatterbot.corpus.english")

# Allena il bot con il dizionario inglese dei saluti
chatbot.train("chatterbot.corpus.english.greetings")

# Allena il bot con il dizionario inglese delle conversazioni
chatbot.train("chatterbot.corpus.english.conversations")
```

**Miglioramenti del corpus da parte degli utenti sono i benvenuti! Fate una pull request.**

# [Documentazione](http://chatterbot.readthedocs.io/)

Leggete la [documentazione](http://chatterbot.readthedocs.io/)
di ChatterBot su Read the Docs.

Per creare voi stessi la documentazione usando [Sphinx](http://www.sphinx-doc.org/), girate:

```
sphinx-build -b html docs/ build/
```

# Esempi

Per leggere qualche esempio, vedete la cartella [esempi](https://github.com/gunthercox/ChatterBot/tree/master/examples).

Abbiamo incluso anche un esempio di un [progetto Django che usa ChatterBot](https://github.com/gunthercox/django_chatterbot), così come un esempio di un [progetto Flask che usa ChatterBot](https://github.com/chamkank/flask-chatterbot).

# Storia

Vedete le note di rilascio per i cambiamenti: https://github.com/gunthercox/ChatterBot/releases

# Passi per contribuire allo sviluppo

1. [Create un fork](https://help.github.com/articles/fork-a-repo/) del [repo principale di ChatterBot](https://github.com/gunthercox/ChatterBot) su GitHub.
2. Implementate i vostri cambiamenti in una branch diversa da `master` (ad esempio, create una branch chiamata `nuove-modifiche`.
3. [Create una pull request](https://help.github.com/articles/creating-a-pull-request/).
4. Per favore, seguite le [linee guida sullo stile di Python per PEP-8](https://www.python.org/dev/peps/pep-0008/).
5. Usate la [funzione di test automatico](http://chatterbot.readthedocs.io/en/latest/testing.html) del progetto per assicurarvi che il vostro contributo sia privo di errori.
