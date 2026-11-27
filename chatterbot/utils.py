"""
ChatterBot utility functions
"""
from typing import TYPE_CHECKING, Any
from chatterbot.conversation import Statement
import importlib
import time

if TYPE_CHECKING:
    from chatterbot.chatterbot import ChatBot


def import_module(dotted_path: str) -> Any:
    """
    Imports the specified module based on the
    dot notated import path for the module.
    """
    module_parts = dotted_path.split('.')
    module_path = '.'.join(module_parts[:-1])
    module = importlib.import_module(module_path)

    return getattr(module, module_parts[-1])


def initialize_class(
    data: dict[str, Any] | str,
    *args: Any,
    **kwargs: Any
) -> Any:
    """
    :param data: A string or dictionary containing a import_path attribute.
    """
    if isinstance(data, dict):
        import_path = data.get('import_path')
        data.update(kwargs)
        Class = import_module(import_path)

        return Class(*args, **data)
    else:
        Class = import_module(data)

        return Class(*args, **kwargs)


def validate_adapter_class(
    validate_class: str | dict[str, Any],
    adapter_class: type
) -> None:
    """
    Raises an exception if validate_class is not a
    subclass of adapter_class.

    :param validate_class: The class to be validated.
    :type validate_class: class

    :param adapter_class: The class type to check against.
    :type adapter_class: class

    :raises: Adapter.InvalidAdapterTypeException
    """
    from chatterbot.adapters import Adapter

    # If a dictionary was passed in, check if it has an import_path attribute
    if isinstance(validate_class, dict):

        if 'import_path' not in validate_class:
            raise Adapter.InvalidAdapterTypeException(
                'The dictionary {} must contain a value for "import_path"'.format(
                    str(validate_class)
                )
            )

        # Set the class to the import path for the next check
        validate_class = validate_class.get('import_path')

    if not issubclass(import_module(validate_class), adapter_class):
        raise Adapter.InvalidAdapterTypeException(
            '{} must be a subclass of {}'.format(
                validate_class,
                adapter_class.__name__
            )
        )


def get_response_time(
    chatbot: 'ChatBot',
    statement: Statement | str | dict[str, Any] | None = 'Hello'
) -> float:
    """
    Returns the amount of time taken for a given
    chat bot to return a response.

    :param chatbot: A chat bot instance.
    :type chatbot: ChatBot

    :returns: The response time in seconds.
    """
    start_time = time.time()

    chatbot.get_response(statement)

    return time.time() - start_time


def get_model_for_language(language: type) -> str:
    """
    Returns the spacy model for the specified language.
    """
    from chatterbot import constants

    try:
        model = constants.DEFAULT_LANGUAGE_TO_SPACY_MODEL_MAP[language]
    except KeyError as e:
        if hasattr(language, 'ENGLISH_NAME'):
            language_name = language.ENGLISH_NAME
        else:
            language_name = language
        raise KeyError(
            f'A corresponding spacy model for "{language_name}" could not be found.'
        ) from e

    return model
