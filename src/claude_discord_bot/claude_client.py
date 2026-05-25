"""Wrapper around the Anthropic API."""

import logging

from anthropic import (
    Anthropic,
    APIConnectionError,
    APIStatusError,
    RateLimitError,
)

log = logging.getLogger(__name__)

_DEFAULT_SYSTEM_PROMPT = (
    "Tu es un bot Discord. "
    "Limite tes réponses à 2000 caractères maximum. "
    "Reste professionnel et évite les blagues ou les réponses trop familières. "
    "En cas de doute, indique-le clairement plutôt que d'inventer une réponse. "
    "Chaque réponse doit être signée par un miaulement."
)


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
                system=system or _DEFAULT_SYSTEM_PROMPT,
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
            log.error(
                "API error status_code=%s error_type=%s",
                e.status_code,
                type(e).__name__,
            )
            return "Une erreur est survenue."
