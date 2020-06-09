def info(text):
    print(
        "[\033[1m\033[32m+\033[0m] {}".format(
            text
        )
    )


def prompt(text, lowercase=True):
    question = raw_input(
        "[\033[1m\033[36m?\033[0m] {}: ".format(
            text
        )
    )
    if lowercase:
        return question.lower()
    return question


def error(text):
    print(
        "[\033[1m\033[31m!\033[0m] {}".format(
            text
        )
    )


def warning(text):
    print(
        "[\033[1m\033[33m-\033[0m] {}".format(
            text
        )
    )


def misc_info(text):
    print(
        "[\033[90mi\033[0m] {}".format(
            text
        )
    )