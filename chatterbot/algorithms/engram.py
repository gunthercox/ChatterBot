def engram(chatbot, text):
    """
    Takes a chatbot object and a statement object.
    Returns a response based on the closest match based on in known conversations.
    """
    from bson import ObjectId
    from fuzzywuzzy import fuzz

    statements = chatbot.database.statements

    closest_statement = statements.find()[0]
    closest_ratio = 0

    for statement in statements.find():
        ratio = fuzz.ratio(statement["text"], text)

        responces_exist = statements.find(
            {"in_response_to": statement["_id"]}
        ).count() > 0

        if ratio > closest_ratio:
            if responces_exist:
                closest_ratio = ratio
                closest_statement = statement

        # If equal ratios, choose the one that has the greatest number of occurances
        elif ratio == closest_ratio:
            if responces_exist:
                if statement["occurrences"] > closest_statement["occurrences"]:
                    closest_statement = statement

    # Select all statements which have been used to respond to this object
    possible_responses = statements.find(
        {"in_response_to": ObjectId(closest_statement["_id"])}
    ).sort("occurrences", -1)

    # Return the response with the greatest number of occurances
    return possible_responses[0]
