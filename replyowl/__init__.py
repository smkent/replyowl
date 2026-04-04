"""Email reply body generator for HTML and text in Python."""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as import_version

from .replyowl import ReplyOwl

try:
    version = import_version(__name__)
except PackageNotFoundError:  # pragma: no cover
    version = "0.0.0"

__all__ = ["ReplyOwl", "version"]
