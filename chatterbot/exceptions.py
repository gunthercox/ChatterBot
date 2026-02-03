class OptionalDependencyImportError(ImportError):
    """
    An exception raised when a feature requires an optional dependency to be installed.
    """
    pass


class SecurityException(Exception):
    """
    Raised when security scanners detect violations.

    This exception is raised when llm-guard security scanners identify threats
    such as prompt injection, toxic content, or sensitive information in user input
    or bot output.

    Attributes:
        violations (list): List of violation details from security scanners.
                          Each violation is a dict containing scanner name,
                          risk score, and affected text.

    Example:
        try:
            response = bot.get_response(user_input)
        except SecurityException as e:
            print(f"Security violation: {e}")
            for violation in e.violations:
                print(f"Scanner: {violation['scanner']}, Risk: {violation['risk_score']}")
    """
    def __init__(self, message, violations=None):
        super().__init__(message)
        self.violations = violations or []
