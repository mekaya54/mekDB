"""
Application settings and configuration helpers.

This module centralizes configuration values used across the backend
modules. Values are loaded from environment variables where appropriate.
"""
from os import getenv

# Database defaults (can be overridden by environment variables)
DB_HOST = getenv("DB_HOST", "localhost")
DB_NAME = getenv("DB_NAME", "imdb_project")
DB_USER = getenv("DB_USER", "root")
DB_PASS = getenv("DB_PASS", "")

# API settings
DEFAULT_LIMIT = int(getenv("DEFAULT_LIMIT", "50"))

# Export a small helper for converting incoming type filters to groups
TYPE_GROUPS = {
	"movie": ["movie", "tvMovie"],
	"tvseries": ["tvSeries", "tvMiniSeries"],
	"tvepisode": ["tvEpisode"],
}

__all__ = [
	"DB_HOST",
	"DB_NAME",
	"DB_USER",
	"DB_PASS",
	"DEFAULT_LIMIT",
	"TYPE_GROUPS",
]
