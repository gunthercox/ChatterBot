'''
Check for online mentions on social media sites.
The bot will follow the user who mentioned it and
favorite the post in which the mention was made.
'''

from chatterbot.apis.twitter import Twitter

chatbot = ChatBot("ChatterBot")

if "twitter" in kwargs:
    twitter_bot = Twitter(kwargs["twitter"])

    for mention in twitter_bot.get_mentions():

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

            follow(screen_name)
            favorite(mention["id"])
            reply(mention["id"], response)
