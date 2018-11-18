def get_recent_repeated_responses(chatbot, conversation, sample=10, threshold=3, quantity=3):
    """
    A filter that eliminates possibly repetitive responses to prevent
    a chat bot from repeating statements that it has recently said.
    """
    from collections import Counter

    # Get the most recent statements from the conversation
    conversation_statements = list(chatbot.storage.filter(
        conversation=conversation,
        order_by=['id']
    ))[sample * -1:]

    text_of_recent_responses = [
        statement.text for statement in conversation_statements
    ]

    counter = Counter(text_of_recent_responses)

    # Find the n most common responses from the conversation
    most_common = counter.most_common(quantity)

    return [
        counted[0] for counted in most_common
        if counted[1] >= threshold
    ]
