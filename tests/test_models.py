import pytest
from pydantic import TypeAdapter, ValidationError

from honeydew_learning.models import WindowInfo

adapter = TypeAdapter(list[WindowInfo])

def test_valid_window_json() -> None:
    sample_json = """
    [
        {
            "id": 19533,
            "application": "ChatGPT",
            "bundleID": "com.openai.codex"
        }
    ]
    """

    windows = adapter.validate_json(sample_json)

    assert len(windows) == 1
    assert windows[0].id == 19533
    assert windows[0].application == "ChatGPT"
    assert windows[0].bundleID == "com.openai.codex"

def test_missing_bundle_id() -> None:
    sample_json = """
    [
        {
            "id": 19533,
            "application": "ChatGPT"
        }
    ]
    """

    with pytest.raises(ValidationError):
        adapter.validate_json(sample_json)


def test_invalid_window_id_type() -> None:
    sample_json = """
    [
        {
            "id": "Hello",
            "application": "ChatGPT"
        }
    ]
    """

    with pytest.raises(ValidationError):
        adapter.validate_json(sample_json)


def test_negative_window_id() -> None:
    sample_json = """
    [
        {
            "id": -1,
            "application": "ChatGPT"
        }
    ]
    """

    with pytest.raises(ValidationError):
        adapter.validate_json(sample_json)




