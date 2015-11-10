'''
Respond to mentions on twitter.
The bot will follow the user who mentioned it and
favorite the post in which the mention was made.
'''

chatbot = ChatBot("ChatterBot",
    storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
    logic_adapter="chatterbot.adapters.logic.ClosestMatchAdapter",
    io_adapter="chatterbot.adapters.io.TwitterAdapter",
    database="../database.db")

for mention in chatbot.get_mentions():

    '''
    Check to see if the post has been favorited
    We will use this as a check for whether or not to respond to it.
    Only respond to unfavorited mentions.
    '''

    if not mention["favorited"]:
        screen_name = mention["user"]["screen_name"]
        text = mention["text"]
        response = chatbot.get_response(text)

        print(text)
        print(response)

        chatbot.follow(screen_name)
        chatbot.favorite(mention["id"])
        chatbot.reply(mention["id"], response)
