class StatementGraph(object):
    """
    This object is a wrapper around chatterbot's storage backend
    that makes it more convenient to traverse known statements as
    a tree-like data structure.
    """

    def __init__(self, storage):
        self.storage = storage

    def get_child_nodes(self, statement):
        return self.storage.filter(in_response_to__contains=statement.text)

    def get_parent_nodes(self, statement):
        return self.storage.find(statement.text).in_response_to


def list_close_matches_for_statements(statements, all_known_statements, max_close_entries=10):
    """
    Takes a list of statements and returns a dictionary where each key is
    the index of the statement in the list, and each value is a list of tuples.
    The first element of each tuple is the closeness that the statement matched,
    and the second value of the tuple is the statement that matched.
    The tuples in the list represent the top selection of most closely matching
    statements.
    """
    close_entries = {}

    for known_statement in all_known_statements:
        for index, statement in enumerate(statements):
            closeness = known_statement.compare_to(statement)

            if index not in close_entries:
                close_entries[index] = []

            close_entries[index].append((closeness, known_statement))

            if len(close_entries[index]) >= max_close_entries:

                # Sort the list by the closeness value
                close_entries[index].sort(key=lambda tup: tup[0])

                # Remove the least-close vlaue from the list
                del close_entries[index][0]

    return close_entries


def get_max_comparison(match_statement, statements):
    max_value = -1
    max_statement = None

    for statement in statements:
        value = match_statement.compare_to(statement)

        if value > max_value:
            max_value = value
            max_statement = statement

    return max_value, max_statement


def backtrack(storage, statement, conversation, max_search_distance):
    return 0, []


def recursive_forward_best_match(graph, start_statement, search_statement, max_search_distance):

    # Return the closeness of the response that has the greatest closeness
    # to one of the next statements in the search sequence

    stack = [(start_statement, [start_statement])]

    while stack:
        (vertex, path) = stack.pop()
        max_comparison = -1
        for next in set(graph.get_child_nodes(vertex)) - set(path):
            comparison = next.compare_to(search_statement)
            if comparison > max_comparison:
                max_comparison = comparison
                yield comparison, path + [next]
            else:
                stack.append((next, path + [next]))
        #max_search_distance -= 1


def foretrack(graph, statement, conversation, max_search_distance):

    if len(conversation) == 1:

        # Check ahead a depth of max_search_distance nodes to see if a closer match to the statement exists
        best_match = list(recursive_forward_best_match(
            graph, statement, conversation[0], max_search_distance
        ))

        if len(best_match) > 1:
            # TODO: Will this ever be the case?
            print "best_match was > 1:", best_match
        print ">>>", best_match

        max_comparison_value, max_comparison = best_match[0]

        return max_comparison_value, [max_comparison]

    return foretrack(graph, statement, conversation[1:], max_search_distance - 1)


def find_sequence_in_tree(storage, conversation, max_depth=100, max_search_distance=0):
    """
    Method to find the closest match to a sequence of strings in
    a tree-like data structure.

    Find the closest match to a sequence S1 l1 S2 l2 S3 l3 ... Sn where each
    Sx is an element in the list S at an index of x and where l is some number
    of S-like elements between 0 and max. Allow the case that some Sx may not
    exist.
    """
    graph = StatementGraph(storage)
    all_known_statements = storage.filter()

    # First, create a list of possible close matches for each statement in the conversation
    matching_data = list_close_matches_for_statements(conversation, all_known_statements)

    for index, statement in enumerate(conversation):
        matches = matching_data[index]

        best_count = -1
        best_match = None

        for match in matches:

            match_value, match_statement = match

            count_ahead = 0
            count_behind = 0
            statements_ahead = []
            statements_behind = []

            if index != 0:
                # Forwards-track to check for the highest number of statements that
                # also have a close match to next elements in the conversation.
                next_conversation_parts = conversation[-1 * (index - 1):]
                count_ahead, statements_ahead = foretrack(graph, match_statement, next_conversation_parts, max_search_distance)

            if index != len(conversation):
                # Backtrack to check for the highest number of statements that
                # also have a close match to previous elements in the conversation.
                previous_conversation_parts = conversation[:index]
                count_behind, statements_behind = backtrack(storage, match_statement, previous_conversation_parts, max_search_distance)

            # Create a sum of the closeness of each of the adjacent element's closeness
            count = count_ahead + count_behind

            if count > best_count:
                count = best_count

                # Join the lists together to get the origional conversation
                best_match = statements_behind + [match] + statements_ahead

    return best_match
