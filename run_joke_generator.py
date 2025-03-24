#!/usr/bin/env python3
"""Simple script to run the joke generator."""

from pytemplate.presenter import JokePresenter
from pytemplate.controller import JokeController
from pytemplate.model import JokeModel
import sys
import os

# Add the source directory to the path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "src")))


def main():
    """Run the joke generator."""
    model = JokeModel()
    controller = JokeController(model)

    # Just get and display a joke
    joke = controller.get_joke()
    print(f"Here's a joke for you: {joke}")

    # Alternatively, use the presenter
    # presenter = JokePresenter(controller)
    # presenter.display_joke()


if __name__ == "__main__":
    main()
