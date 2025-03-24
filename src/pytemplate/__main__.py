"""Main entry point for the joke generator."""

from pytemplate.presenter import JokePresenter


def main() -> None:
    """Run the joke generator application."""
    presenter = JokePresenter()
    presenter.run_cli()


if __name__ == "__main__":
    main()
