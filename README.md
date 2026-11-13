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

## License

License to be determined.
