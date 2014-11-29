def engram(text, log_directory):
    """
    Takes a message from a conversation.
    Returns a response based on the closest match based on in known conversations.
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

    # Seek a better response if the difference ratio is too low or the choice list is empty
    if (not closest_response) or (closest_ratio < 90):
        # TODO Search the web or use other algorithms
        pass

    if not closest_response:
        default = Statement("Error", "No possible replies could be determined.")
        return [default]

    return closest_response
