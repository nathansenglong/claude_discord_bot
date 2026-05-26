FROM python:3.12-slim AS builder
WORKDIR /app
COPY pyproject.toml .
COPY src/ ./src/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -e ".[dev]"

FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY src/ ./src/

RUN useradd --no-create-home --shell /bin/false botuser
USER botuser

CMD ["python", "-m", "claude_discord_bot.bot"]
