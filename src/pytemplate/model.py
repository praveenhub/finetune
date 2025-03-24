"""Model for joke generation."""

from dataclasses import dataclass, field
from typing import List
import random
import secrets


@dataclass
class JokeModel:
    """Model for storing and retrieving jokes.

    Attributes:
        jokes: List of jokes
    """

    jokes: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Initialize with some default jokes if none provided."""
        if not self.jokes:
            self.jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the Python programmer wear glasses? Because they couldn't C#",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
                "There are 10 types of people in the world: those who understand binary and those who don't.",
                "Why was the JavaScript developer sad? Because they didn't Node how to Express themselves.",
            ]

    def get_random_joke(self) -> str:
        """Get a random joke from the collection.

        Returns:
            A random joke string
        """
        # Use secrets module for more secure randomness
        return self.jokes[secrets.randbelow(len(self.jokes))]

    def add_joke(self, joke: str) -> None:
        """Add a new joke to the collection.

        Args:
            joke: The joke to add
        """
        self.jokes.append(joke)
