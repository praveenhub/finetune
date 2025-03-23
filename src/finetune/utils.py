"""Utility functions for the package."""

import logging
import os
from typing import Any, cast


def setup_logger(name: str = "project", level: int = logging.INFO, log_file: str | None = None) -> logging.Logger:
    """Set up a logger with the given name and level.

    Args:
        name: Logger name
        level: Logging level
        log_file: Optional file to write logs to

    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


class ConfigError(FileNotFoundError):
    """Exception raised for configuration file errors."""

    def __init__(self, path: str) -> None:
        super().__init__(f"Config file not found: {path}")


class UnsupportedFormatError(ValueError):
    """Exception raised for unsupported file formats."""

    def __init__(self, format_path: str) -> None:
        super().__init__(f"Unsupported config format: {format_path}")


class YAMLRequiredError(ImportError):
    """Exception raised when PyYAML is required but not installed."""

    def __init__(self) -> None:
        super().__init__("PyYAML is required to load YAML configs.")


def load_config(config_path: str) -> dict[str, Any]:
    """Load configuration from a file.

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration dictionary

    Raises:
        ConfigError: If the config file is not found
        UnsupportedFormatError: If the config file format is not supported
        YAMLRequiredError: If YAML is required but PyYAML is not installed
    """
    if not os.path.exists(config_path):
        raise ConfigError(config_path)

    # Check file extension and load accordingly
    if config_path.endswith(".json"):
        import json

        with open(config_path) as f:
            return cast(dict[str, Any], json.load(f))
    elif config_path.endswith((".yml", ".yaml")):
        try:
            import yaml

            with open(config_path) as f:
                return cast(dict[str, Any], yaml.safe_load(f))
        except ImportError as err:
            raise YAMLRequiredError() from err
    else:
        raise UnsupportedFormatError(config_path)
