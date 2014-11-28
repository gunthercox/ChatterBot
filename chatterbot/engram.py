from conversation import Conversation


class Engram(object):

    def engram(self, text, log_directory):
        """
        Takes a message from a conversation.
        Returns the closest match based on known conversations.
        """
        import os

        # Check to make sure that valid text was passed in
        text = str(text)
        if not text.strip():
            return "No text input was provided."

        closest_response = None
        closest_ratio = 0

        for log in os.listdir(log_directory):
            path = log_directory + "/" + log

            conversation = Conversation()
            conversation.read(path)
            response, ratio = conversation.find_closest_response(text)

            if ratio > closest_ratio:
                closest_response = response
                closest_ratio = ratio

        if not closest_response:
            return "Error, no possible replies could be determined."

        return closest_response[0].text

