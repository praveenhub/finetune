"""Tests for the joke generator MCP implementation."""

from unittest.mock import MagicMock

from pytemplate.controller import JokeController
from pytemplate.model import JokeModel
from pytemplate.presenter import JokePresenter


class TestJokeModel:
    """Tests for the JokeModel class."""

    def test_init_with_default_jokes(self) -> None:
        """Test that model initializes with default jokes when none provided."""
        model = JokeModel()
        assert len(model.jokes) > 0

    def test_init_with_custom_jokes(self) -> None:
        """Test that model initializes with provided jokes."""
        custom_jokes = ["Custom joke 1", "Custom joke 2"]
        model = JokeModel(jokes=custom_jokes)
        assert model.jokes == custom_jokes

    def test_get_random_joke(self) -> None:
        """Test that get_random_joke returns a joke from the list."""
        jokes = ["Joke 1", "Joke 2", "Joke 3"]
        model = JokeModel(jokes=jokes)
        joke = model.get_random_joke()
        assert joke in jokes

    def test_add_joke(self) -> None:
        """Test that add_joke adds a joke to the list."""
        model = JokeModel(jokes=["Initial joke"])
        model.add_joke("New joke")
        assert "New joke" in model.jokes
        assert len(model.jokes) == 2


class TestJokeController:
    """Tests for the JokeController class."""

    def test_get_joke(self) -> None:
        """Test that get_joke returns a joke from the model."""
        mock_model = MagicMock()
        mock_model.get_random_joke.return_value = "Mock joke"

        controller = JokeController(model=mock_model)
        joke = controller.get_joke()

        assert joke == "Mock joke"
        mock_model.get_random_joke.assert_called_once()

    def test_add_joke_valid(self) -> None:
        """Test that add_joke adds a valid joke to the model."""
        mock_model = MagicMock()

        controller = JokeController(model=mock_model)
        result = controller.add_joke("This is a valid joke")

        assert result is True
        mock_model.add_joke.assert_called_once_with("This is a valid joke")

    def test_add_joke_invalid(self) -> None:
        """Test that add_joke rejects invalid jokes."""
        mock_model = MagicMock()

        controller = JokeController(model=mock_model)
        result = controller.add_joke("Short")

        assert result is False
        mock_model.add_joke.assert_not_called()


class TestJokePresenter:
    """Tests for the JokePresenter class."""

    def test_display_joke(self) -> None:
        """Test that display_joke gets a joke from controller and displays it."""
        mock_controller = MagicMock()
        mock_controller.get_joke.return_value = "Test joke"

        mock_display = MagicMock()

        presenter = JokePresenter(controller=mock_controller, display_callback=mock_display, error_callback=MagicMock())

        presenter.display_joke()

        mock_controller.get_joke.assert_called_once()
        mock_display.assert_called_once_with("Here's a joke for you: Test joke")

    def test_add_joke_valid(self) -> None:
        """Test that add_joke with valid joke calls controller and displays success."""
        mock_controller = MagicMock()
        mock_controller.add_joke.return_value = True

        mock_display = MagicMock()
        mock_error = MagicMock()

        presenter = JokePresenter(controller=mock_controller, display_callback=mock_display, error_callback=mock_error)

        presenter.add_joke("Valid joke")

        mock_controller.add_joke.assert_called_once_with("Valid joke")
        mock_display.assert_called_once_with("Joke added successfully!")
        mock_error.assert_not_called()

    def test_add_joke_invalid(self) -> None:
        """Test that add_joke with invalid joke displays error."""
        mock_controller = MagicMock()
        mock_controller.add_joke.return_value = False

        mock_display = MagicMock()
        mock_error = MagicMock()

        presenter = JokePresenter(controller=mock_controller, display_callback=mock_display, error_callback=mock_error)

        presenter.add_joke("Invalid")

        mock_controller.add_joke.assert_called_once_with("Invalid")
        mock_display.assert_not_called()
        mock_error.assert_called_once()
