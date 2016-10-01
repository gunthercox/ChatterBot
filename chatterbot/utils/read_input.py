import sys


def input_function():
    """
    Normalizes reading input between python 2 and 3.
    The function 'raw_input' becomes 'input' in Python 3.
    """
    if sys.version_info[0] < 3:
        user_input = str(raw_input())

        # Avoid problems using format strings with unicode characters
        if user_input:
            user_input = user_input.decode('utf-8')

    else:
        user_input = input()
        
    return user_input
