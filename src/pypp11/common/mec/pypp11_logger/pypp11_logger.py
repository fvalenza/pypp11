""" This module makes available logging capability
"""

_log_format = "{: <10s}| {}"


def error(message, enabled=True):
  if enabled:
    print(_log_format.format("Error", message))


def warning(message, enabled=True):
  if enabled:
    print(_log_format.format("Warning", message))


def info(message, enabled=True):
  if enabled:
    print(_log_format.format("Info", message))


def debug(message, enabled=True):
  if enabled:
    print(_log_format.format("Debug", message))


__all__ = ["error", "warning", "info", "debug"]
