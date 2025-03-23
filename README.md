# finetune

[![Release](https://img.shields.io/github/v/release/praveenhub/finetune)](https://img.shields.io/github/v/release/praveenhub/finetune)
[![Build status](https://img.shields.io/github/actions/workflow/status/praveenhub/finetune/main.yml?branch=main)](https://github.com/praveenhub/finetune/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/praveenhub/finetune/branch/main/graph/badge.svg)](https://codecov.io/gh/praveenhub/finetune)
[![Commit activity](https://img.shields.io/github/commit-activity/m/praveenhub/finetune)](https://img.shields.io/github/commit-activity/m/praveenhub/finetune)
[![License](https://img.shields.io/github/license/praveenhub/finetune)](https://img.shields.io/github/license/praveenhub/finetune)

A Python package for fine-tuning machine learning models with a clean, modular interface.

- **Github repository**: <https://github.com/praveenhub/finetune/>
- **Documentation**: <https://praveenhub.github.io/finetune/>

## Features

- Generic model fine-tuning interface that works with various ML frameworks
- Flexible configuration management
- Command-line interface for easy experimentation
- Comprehensive logging and metrics tracking
- Type hints and thorough documentation
- Extensive test coverage

## Installation

### From PyPI

```bash
pip install finetune
```

### With Optional Dependencies

```bash
# With PyTorch integration
pip install "finetune[torch]"

# With Transformers support
pip install "finetune[transformers]"

# With all optional dependencies
pip install "finetune[all]"
```

### Development Installation

```bash
git clone https://github.com/praveenhub/finetune.git
cd finetune
make install
```

## Quick Start

Here's a simple example of how to use finetune:

```python
from finetune import Model, Trainer, set_seed

# Set seed for reproducibility
set_seed(42)

# Create a model
model = Model(name="my_model")

# Create a trainer with default configuration
trainer = Trainer(model)

# Load your data (numpy arrays)
import numpy as np
features = np.random.rand(100, 10)  # 100 samples, 10 features
labels = np.random.randint(0, 2, size=(100,))  # Binary labels

# Train the model
metrics = trainer.train(features, labels)

# Make predictions
predictions = model.predict(features)
```

## Command Line Interface

The package includes a CLI for training and making predictions:

```bash
# Train a model
finetune train --model my_model --train-data path/to/train.csv --val-data path/to/val.csv

# Make predictions
finetune predict --model path/to/saved/model --data path/to/test.csv --output predictions.json
```

## Docker

A Docker image is available for running finetune in an isolated environment:

```bash
# Build the Docker image
docker build -t finetune .

# Run the container
docker run -it --rm finetune
```

## Contributing

Contributions are welcome! Please check out our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Install development dependencies
make install

# Run tests
make test

# Run linting
make lint

# Run type checking
make mypy
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
