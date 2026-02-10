"""Streamlit entrypoint shim that keeps backward compatibility with tools
looking for ``techdocsbench/app.py`` while the actual UI still lives at
``src/app.py``."""

from __future__ import annotations

import runpy
from pathlib import Path

_ROOT_APP = Path(__file__).resolve().parents[1] / "app.py"


def main() -> None:
    """Execute the real Streamlit app module."""
    runpy.run_path(str(_ROOT_APP), run_name="__main__")


if __name__ == "__main__":
    main()