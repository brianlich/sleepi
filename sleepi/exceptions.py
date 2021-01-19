
"""Exceptions for Elgato Key Lights."""


class SleepiError(Exception):
    """Generic Elgato Key Light exception."""

class SleepiConnectionError(SleepiError):
    """Elgato Key Light connection exception."""


class SleepiGenericError(Exception):
    """Generic WLED exception."""