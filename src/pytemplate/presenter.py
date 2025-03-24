"""Presenter for joke generator application."""

from typing import Callable, List, Optional

from pytemplate.controller import JokeController


class JokePresenter:
    """Presenter for joke generator application.

    This class handles the presentation logic and user interaction.

    Attributes:
        controller: The joke controller
        display_callback: Function to display output to the user
        error_callback: Function to display errors to the user
    """

    def __init__(
        self,
        controller: Optional[JokeController] = None,
        display_callback: Optional[Callable[[str], None]] = None,
        error_callback: Optional[Callable[[str], None]] = None
    ) -> None:
        """Initialize the presenter.

        Args:
            controller: Optional controller, creates a new one if not provided
            display_callback: Function to display output to the user
            error_callback: Function to display errors to the user
        """
        self.controller = controller or JokeController()
        self.display_callback = display_callback or print
        self.error_callback = error_callback or print

    def display_joke(self) -> None:
        """Display a random joke to the user."""
        joke = self.controller.get_joke()
        self.display_callback(f"Here's a joke for you: {joke}")

    def add_joke(self, joke: str) -> None:
        """Add a new joke if valid.

        Args:
            joke: The joke to add
        """
        if self.controller.add_joke(joke):
            self.display_callback("Joke added successfully!")
        else:
            self.error_callback(
                "Invalid joke! Jokes must be at least 10 characters long.")

    def run_cli(self) -> None:
        """Run an interactive command-line interface."""
        commands = {
            "1": ("Get a joke", self.display_joke),
            "2": ("Add a joke", lambda: self.add_joke(input("Enter your joke: "))),
            "3": ("Exit", None)
        }

        while True:
            self.display_callback("\nJoke Generator Menu:")
            for key, (description, _) in commands.items():
                self.display_callback(f"{key}. {description}")

            choice = input("\nEnter your choice (1-3): ")

            if choice not in commands:
                self.error_callback("Invalid choice. Please try again.")
                continue

            if choice == "3":
                self.display_callback("Goodbye!")
                break

            commands[choice][1]()  # Execute the selected function
