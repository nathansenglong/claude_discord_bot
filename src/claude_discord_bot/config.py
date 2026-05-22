"""Configuration loaded from environment variables."""
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    """Immutable configuration object for the bot."""

    anthropic_api_key: str
    discord_bot_token: str
    claude_model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 1024

    @classmethod
    def from_env(cls) -> "Config":
        """Load config from environment variables."""
        try:
            return cls(
                anthropic_api_key=os.environ["ANTHROPIC_API_KEY"],
                discord_bot_token=os.environ["DISCORD_BOT_TOKEN"],
                claude_model=os.environ.get(
                    "CLAUDE_MODEL", "claude-sonnet-4-20250514"
                ),
            )
        except KeyError as e:
            raise RuntimeError(f"Missing required env var: {e}") from e