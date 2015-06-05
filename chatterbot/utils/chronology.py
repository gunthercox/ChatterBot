import datetime


def timestamp(fmt="%Y-%m-%d-%H-%M-%S"):
    """
    Returns a string formatted timestamp of the current time.
    """
    return datetime.datetime.now().strftime(fmt)
