from chatterbot import Terminal, TalkWithCleverbot


#talk = TalkWithCleverbot()
#talk.begin()

terminal = Terminal()
terminal.log_directory="conversation_engrams/"

#from settings import TWITTER
#terminal.enable_twitter_api(TWITTER["CONSUMER_KEY"], TWITTER["CONSUMER_SECRET"])

terminal.begin()
