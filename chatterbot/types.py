def engram(text, log_directory):
    """
    Takes a message from a conversation.
    Returns the closest match based on known conversations.
    """
    from chatterbot.conversation import Statement, Conversation
    import os

    closest_response = None
    closest_ratio = 0

    for log in os.listdir(log_directory):
        path = log_directory + "/" + log

        if os.path.isfile(path):

            conversation = Conversation()
            conversation.read(path)
            response, ratio = conversation.find_closest_response(text)

            if ratio > closest_ratio:
                closest_response = response
                closest_ratio = ratio

    if not closest_response:
        default = Statement("error", "No possible replies could be determined.")
        return [default]

    return closest_response
