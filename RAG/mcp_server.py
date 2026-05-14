from __future__ import annotations

import sys
import os

# Allow running from the RAG/ directory: `python mcp_server.py`
sys.path.insert(0, os.path.dirname(__file__))

from typing import Any

from mcp.server.fastmcp import FastMCP

from app.libs.elasticsearch_db import get_elastic_db

mcp = FastMCP("docs-rag")


@mcp.tool()
def list_docs() -> list[dict[str, Any]]:
    """List all available documentation files that have been indexed and can be searched.

    Returns a list of all markdown files in the index, with their relative path,
    filename, number of indexed chunks, and a one-line summary taken from the
    first chunk. Use this to discover what docs exist before deciding which one
    to search or retrieve.

    Returns:
        List of dicts, each with:
          - file: bare filename (e.g. "architecture.md")
          - path: source path as stored at ingest time (e.g. "docs/architecture.md")
          - chunks: number of indexed chunks for this file
          - summary: first line of the first chunk, or null if unavailable
    """
    return get_elastic_db().list_docs()


if __name__ == "__main__":
    mcp.run()
