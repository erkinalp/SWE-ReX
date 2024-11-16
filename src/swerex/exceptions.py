class SWEReXception(Exception):
    """Any exception that is raised by SWE-ReX."""


class SessionNotInitializedError(SWEReXception, RuntimeError):
    """Raised if we try to run a command in a shell that is not initialized."""


class NonZeroExitCodeError(SWEReXception, RuntimeError):
    """Can be raised if we execute a command in the shell and it has a non-zero exit code."""


class BashIncorrectSyntaxError(SWEReXception, RuntimeError):
    """Before running a bash command, we check for syntax errors.
    This is the error message for those syntax errors.
    """


class CommandTimeoutError(SWEReXception, RuntimeError, TimeoutError): ...


class NoExitCodeError(SWEReXception, RuntimeError): ...


class SessionExistsError(SWEReXception, ValueError): ...


class SessionDoesNotExistError(SWEReXception, ValueError): ...


class DeploymentNotStartedError(SWEReXception, RuntimeError):
    def __init__(self, message="Deployment not started"):
        super().__init__(message)
