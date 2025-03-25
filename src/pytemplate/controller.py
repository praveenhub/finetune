"""Controller for joke generator application."""

from pytemplate.model import JokeModel


class JokeController:
    """Controller for joke generator application.

    This class handles the business logic for the joke generator.

    Attributes:
        model: The joke data model
    """

    def __init__(self, model: JokeModel | None = None) -> None:
        """Initialize the controller.

        Args:
            model: Optional joke model, creates a new one if not provided
        """
        self.model = model or JokeModel()

    def get_joke(self) -> str:
        """Get a random joke.

        Returns:
            A random joke string
        """
        return self.model.get_random_joke()

    def add_joke(self, joke: str) -> bool:
        """Add a new joke if it's valid.

        Args:
            joke: The joke to add

        Returns:
            True if joke was added, False otherwise
        """
        # Simple validation - joke should be at least 10 characters
        if not joke or len(joke) < 10:
            return False

        self.model.add_joke(joke)
        return True
