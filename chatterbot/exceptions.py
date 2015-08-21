class LoggingDisabledException(Exception):
    def __init__(self, message="Logging is disabled. Set read_only to False to allow training."):
        self.message = message

