#!/usr/bin/env python3
"""Interactive CLI for the joke generator."""

from pytemplate.presenter import JokePresenter
import sys
import os

# Add the source directory to the path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "src")))


def main():
    """Run the interactive joke generator CLI."""
    presenter = JokePresenter()
    presenter.run_cli()


if __name__ == "__main__":
    main()
