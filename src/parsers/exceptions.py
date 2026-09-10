"""
Exceptions for code parsers.
"""

class ParserError(Exception):
    """Base exception for code parsing errors."""
    pass

class UnsupportedSyntaxError(ParserError):
    """Raised when file contains syntax not supported by the parser."""
    pass

class ParserTimeoutError(ParserError):
    """Raised when parsing exceeds allocated time."""
    pass
