"""Package for Python project template."""

__version__ = "0.0.1"

from pytemplate.model import JokeModel
from pytemplate.controller import JokeController
from pytemplate.presenter import JokePresenter
from pytemplate.utils import load_config, setup_logger

__all__ = ["JokeModel", "JokeController",
           "JokePresenter", "load_config", "setup_logger"]
