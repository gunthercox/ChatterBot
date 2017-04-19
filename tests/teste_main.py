from chatterbot import ChatBot

chatbot = ChatBot("Terminal",

                  logic_adapters=[
                      "chatterbot.logic.BestMatch"
                  ],
                  trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
                  input_adapter="chatterbot.input.TerminalAdapter",
                  output_adapter="chatterbot.output.TerminalAdapter",

                  storage_adapter="chatterbot.storage.SQLAlchemyDatabaseAdapter",
                  database_uri="sqlite:///database_test.db", # use database_uri or database, database_uri can be especified to choose database driver
                  database="database_test", # use for sqlite database. Ignored if database_uri especified .
                  read_only=False,  # Readonly database, Default: False
                  drop_create=True  # for recreate database every start read_olny must be False, Default: False
                  )

# Train based on the english corpus
#chatbot.train("chatterbot.corpus.english")

# Train based on english greetings corpus
chatbot.train("chatterbot.corpus.english.greetings")

# Train based on the english conversations corpus
# chatbot.train("chatterbot.corpus.english.conversations")


print("Type something to begin...")

# The following loop will execute each time the user enters input
while True:
    try:
        # We pass None to this method because the parameter
        # is not used by the TerminalAdapter
        bot_input = chatbot.get_response(None)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break