import datetime


class Signature(object):
    """
    Returns ChatterBot's signature.
    """

    def __init__(self, name):
        self.name = name
        self.time = self.create_timestamp()

    def create_timestamp(self, fmt="%Y-%m-%d-%H-%M-%S"):
        """
        Returns a string formatted timestamp of the current time.
        """
        return datetime.datetime.now().strftime(fmt)

    def serialize(self):
        signature = {}

        signature['name'] = self.name
        signature['time'] = self.time

        return signature
