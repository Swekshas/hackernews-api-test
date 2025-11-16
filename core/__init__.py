# core package initializer
# Makes `core` importable as a package for tests and other modules.

from .config import *  # re-export common config if helpful
from .api_client import APIClient

__all__ = ["BASE_URL", "HEADERS", "APIClient"]
