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


def backtrack(storage, statement, max_permutation):
    return 0, []


def fortrack(storage, statement, max_permutation):
    return 0, []


def find_sequence_in_tree(storage, conversation, max_depth=100, max_permutation=0):
    """
    Method to find the closest match to a sequence of strings in
    a tree-like data structure.

    Find the closest match to a sequence S1 l1 S2 l2 S3 l3 ... Sn where each
    Sx is an element in the list S at an index of x and where l is some number
    of S-like elements between 0 and max. Allow the case that some Sx may not
    exist.
    """
    all_known_statements = storage.filter()

    # First, create a list of possible close matches for each statement in the conversation
    matching_data = list_close_matches_for_statements(conversation, all_known_statements)

    for index, statement in enumerate(conversation):
        matches = matching_data[index]

        best_count = -1
        best_match = None

        for match in matches:

            # Forwards-track to check for the highest number of statements that
            # also have a close match to next elements in the conversation.
            count_ahead, statements_ahead = fortrack(storage, match, max_permutation)

            # Backtrack to check for the highest number of statements that
            # also have a close match to previous elements in the conversation.
            count_behind, statements_behind = backtrack(storage, match, max_permutation)

            # Create a sum of the closeness of each of the adjacent element's closeness
            count = count_ahead + count_behind

            if count > best_count:
                count = best_count

                # Join the lists together to get the origional conversation
                best_match = statements_behind + [match] + statements_ahead

    return best_match
