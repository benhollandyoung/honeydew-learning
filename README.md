# 🍈 Honeydew

**Turn what you see into what you remember.**

Honeydew is an open-source, local-first macOS learning agent designed to turn useful information from your screen into Anki flashcards and short coding exercises.

The goal is to help retain knowledge encountered while working with AI assistants, reading documentation, and learning new concepts.

## Planned features

- On-device screen observation using macOS APIs
- Local language model for topic-aware flashcard generation
- Customisable learning topics
- Coding exercises for software engineering
- Daily CSV export for Anki
- Privacy-first, offline processing

## Development

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run honeydew --help
uv run pytest
uv run ruff check .
uv run mypy src/
```

## Status

**Early development — v0.1.0**

The CLI foundation is implemented. Screen observation, local inference, and Anki export are planned but not yet available.

## Troubleshooting

### `ModuleNotFoundError` when using uv on macOS

On some macOS setups, Python may fail to import Honeydew even after successfully running `uv sync`.

This can occur when macOS marks files inside `.venv` with the `hidden` filesystem flag. Python may consequently skip the `.pth` files used to make the project importable.

**Symptoms:**

- `uv sync` completes successfully.
- `uv run honeydew --help` fails with `ModuleNotFoundError`.
- `uv run pytest` fails to import `honeydew_learning`.

**Workaround:**

From the project root, run:

```bash
chflags -R nohidden .venv
```

Then verify:

```bash
uv run honeydew --help
uv run pytest -v
```

You may need to repeat this workaround if the virtual environment is recreated or the hidden flags reappear.

**Related issue:** [astral-sh/uv#16977](https://github.com/astral-sh/uv/issues/16977).

This is an environment-level issue, not a problem with Honeydew's source code.

## License

License to be determined.
