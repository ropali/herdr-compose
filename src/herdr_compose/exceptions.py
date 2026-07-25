"""Custom exceptions for herdr-compose."""


class HerdrComposeError(Exception):
    """Base exception class for all herdr-compose errors."""

    pass


class ConfigError(HerdrComposeError):
    """Raised when layout configuration loading or validation fails."""

    pass


class HerdrCmdError(HerdrComposeError):
    """Raised when running a herdr subcommand fails."""

    def __init__(self, cmd: list[str], returncode: int, stderr: str):
        self.cmd = cmd
        self.returncode = returncode
        self.stderr = stderr
        message = f"Command 'herdr {' '.join(cmd)}' failed with exit code {returncode}:\n{stderr}"
        super().__init__(message)


class HerdrNotInstalledError(HerdrComposeError):
    """Raised when the 'herdr' executable is not found on PATH."""

    def __init__(self):
        super().__init__(
            "The 'herdr' CLI tool was not found on your PATH. Please ensure Herdr is installed."
        )
