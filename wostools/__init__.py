"""Top-level package for Python WoS tools."""

__author__ = """Core of Science"""
__email__ = "dev@coreofscience.com"
__version__ = "1.1.0"

from wostools.article import Article
from wostools.lazy import CollectionLazy
from wostools.cached import CollectionCached as Collection

__all__ = ["Collection", "CollectionLazy", "Article"]
