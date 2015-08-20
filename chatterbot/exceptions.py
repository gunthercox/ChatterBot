class LoggingDisabledException(Exception):
    def __init__(self, message="Logging is disabled. Enable logging to allow training."):
        self.message = message
