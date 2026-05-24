"""Tests for ClaudeClient — retroactive coverage on the existing wrapper."""

import pytest
from unittest.mock import MagicMock, patch

from anthropic import APIConnectionError, APIStatusError, RateLimitError

from claude_discord_bot.claude_client import ClaudeClient


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_anthropic():
    """Patch the Anthropic constructor in claude_client's module scope."""
    with patch("claude_discord_bot.claude_client.Anthropic") as mock:
        yield mock


@pytest.fixture
def client(mock_anthropic):
    """Return a ClaudeClient wired to the mock Anthropic instance."""
    return ClaudeClient(api_key="test-key", model="claude-test-model")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _make_response(text: str) -> MagicMock:
    """Build a minimal fake anthropic.Message whose content[0].text == text."""
    msg = MagicMock()
    msg.content[0].text = text
    return msg


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_ask_returns_response_text(client, mock_anthropic):
    """Happy path: ask() returns the text field from Claude's response."""
    # Arrange
    mock_anthropic.return_value.messages.create.return_value = _make_response("Bonjour !")
    # Act
    result = client.ask("Dis bonjour")
    # Assert
    assert result == "Bonjour !"


def test_ask_uses_default_system_prompt(client, mock_anthropic):
    """When system=None, the default prompt mentioning 'Discord bot' is used."""
    # Arrange
    mock_anthropic.return_value.messages.create.return_value = _make_response("ok")
    # Act
    client.ask("test")
    # Assert
    kwargs = mock_anthropic.return_value.messages.create.call_args.kwargs
    assert "Discord bot" in kwargs["system"]


def test_ask_uses_custom_system_prompt(client, mock_anthropic):
    """When system is provided, that value is passed verbatim to the API."""
    # Arrange
    mock_anthropic.return_value.messages.create.return_value = _make_response("ok")
    # Act
    client.ask("test", system="Tu es un pirate.")
    # Assert
    kwargs = mock_anthropic.return_value.messages.create.call_args.kwargs
    assert kwargs["system"] == "Tu es un pirate."


def test_ask_passes_model_and_max_tokens(client, mock_anthropic):
    """ask() forwards model and max_tokens from constructor to the API."""
    # Arrange
    mock_anthropic.return_value.messages.create.return_value = _make_response("ok")
    # Act
    client.ask("test")
    # Assert
    kwargs = mock_anthropic.return_value.messages.create.call_args.kwargs
    assert kwargs["model"] == "claude-test-model"
    assert kwargs["max_tokens"] == 1024


def test_ask_handles_rate_limit_error(client, mock_anthropic):
    """RateLimitError is caught and returns a French message containing 'surcharg'."""
    # Arrange
    exc = Exception.__new__(RateLimitError)
    mock_anthropic.return_value.messages.create.side_effect = exc
    # Act
    result = client.ask("test")
    # Assert
    assert "surcharg" in result


def test_ask_handles_connection_error(client, mock_anthropic):
    """APIConnectionError is caught and returns a French message containing 'connexion'."""
    # Arrange
    exc = Exception.__new__(APIConnectionError)
    mock_anthropic.return_value.messages.create.side_effect = exc
    # Act
    result = client.ask("test")
    # Assert
    assert "connexion" in result


def test_ask_handles_api_status_error(client, mock_anthropic):
    """APIStatusError is caught and returns a French message containing 'erreur'."""
    # Arrange
    exc = Exception.__new__(APIStatusError)
    exc.status_code = 500
    mock_anthropic.return_value.messages.create.side_effect = exc
    # Act
    result = client.ask("test")
    # Assert
    assert "erreur" in result
