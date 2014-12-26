def get_closest(text, log_directory, similarity_threshold):
    from chatterbot.conversation import Statement, Conversation
    import os

    closest_response = []
    closest_ratio = 0

    for log in os.listdir(log_directory):
        path = log_directory + "/" + log

        if os.path.isfile(path):
            conversation = Conversation()
            conversation.read(path)
            response, ratio = conversation.find_closest_response(text)

            # A response may not be returned if a log has less than one line
            if response:
                if ratio > closest_ratio:
                    closest_response = []
                    closest_response.append(response)
                    closest_ratio = ratio
                elif ratio == closest_ratio and closest_ratio != 0:
                    closest_response.append(response)
                    closest_ratio = ratio

    return closest_response, closest_ratio

def engram(text, log_directory):
    """
    Takes a message from a conversation.
    Returns a response based on the closest match based on in known conversations.
    """
    import random

    threshold = 90
    closest_response, closest_ratio = get_closest(text, log_directory, threshold)

    if not closest_response:
        from chatterbot.conversation import Statement
        default = Statement("Error", "No possible replies could be determined.")
        return [default]

    return random.choice(closest_response)
