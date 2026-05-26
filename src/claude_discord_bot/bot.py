"""Discord bot entry point."""

import logging

import discord

from .claude_client import ClaudeClient
from .config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger(__name__)


def create_bot(config: Config) -> discord.Client:
    """Create and configure the Discord client."""
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)
    claude = ClaudeClient(
        api_key=config.anthropic_api_key,
        model=config.claude_model,
        max_tokens=config.max_tokens,
    )

    @client.event
    async def on_ready():
        log.info(f"Connected as {client.user}")

    @client.event
    async def on_message(message: discord.Message):
        # Ignore les messages du bot lui-même
        if message.author == client.user:
            return
        # Repond seulement si mentionne
        if client.user not in message.mentions:
            return

        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
        if not prompt:
            await message.reply(
                "Je suis un assistant IA propulsé par **Claude** (Anthropic). "
                "Pose-moi une question !"
            )
            return

        async with message.channel.typing():
            response = claude.ask(prompt)
        await message.reply(response[:2000])  # Discord limit

    return client


def main():
    """Application entry point."""
    config = Config.from_env()
    bot = create_bot(config)
    bot.run(config.discord_bot_token, log_handler=None)


if __name__ == "__main__":
    main()
