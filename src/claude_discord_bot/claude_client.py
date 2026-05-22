"""Wrapper around the Anthropic API."""
import logging

from anthropic import (
    Anthropic,
    APIConnectionError,
    APIStatusError,
    RateLimitError,
)

log = logging.getLogger(__name__)


class ClaudeClient:
    """Wrapper around the Anthropic API with error handling."""

    def __init__(self, api_key: str, model: str, max_tokens: int = 1024):
        self._client = Anthropic(api_key=api_key, max_retries=3, timeout=30.0)
        self._model = model
        self._max_tokens = max_tokens

    def ask(self, prompt: str, system: str | None = None) -> str:
        """Send a prompt to Claude and return the text response."""
        try:
            msg = self._client.messages.create(
                model=self._model,
                max_tokens=self._max_tokens,
                system=system or "You are a helpful Discord bot. Keep replies under 2000 characters.",
                messages=[{"role": "user", "content": prompt}],
            )
            return msg.content[0].text
        except RateLimitError:
            log.warning("Rate limit hit")
            return "Je suis un peu surchargé, réessaie dans quelques secondes."
        except APIConnectionError:
            log.error("Connection error")
            return "Problème de connexion à l'API. Réessaie."
        except APIStatusError as e:
            log.error(f"API error {e.status_code}: {e.message}")
            return "Une erreur est survenue."