import sys


def input_function():
    """
    Normalize reading input between python 2 and 3.
    'raw_input' is just 'input' in python3
    """
    if sys.version_info[0] < 3:
        user_input = str(raw_input())
    else:
        user_input = input()

    if user_input:
        user_input = user_input.decode('utf-8')
        
    return user_input
