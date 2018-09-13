"""
ChatterBot constants
"""

'''
The maximum length of characters that the text of a statement can contain.
This should be enforced on a per-model basis by the data model for each
storage adapter.
'''
STATEMENT_TEXT_MAX_LENGTH = 400

'''
The maximum length of characters that the text label of a conversation can contain.
The number 32 was chosen because that is the length of the string representation
of a UUID4 with no hyphens.
'''
CONVERSATION_LABEL_MAX_LENGTH = 32

# The maximum length of characters that the name of a tag can contain
TAG_NAME_MAX_LENGTH = 50

DEFAULT_DJANGO_APP_NAME = 'django_chatterbot'
