# claude_discord_bot
Projet personnel pour me familiariser avec une stack pro complète : bot Discord prop
ulsé par l'API Claude, développé en Python avec tests automatisés, conteneurisé avec
 Docker, intégré en CI/CD via GitHub Actions et déployé en continu sur Azure. Work
flow git pro (branches, PR, conventional commits).
# claude-discord-bot

[![CI](https://github.com/nathansenglong/claude_discord_bot/actions/workflows/ci.yml
/badge.svg)](https://github.com/nathansenglong/claude_discord_bot/actions/workflows/
ci.yml)
![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue)
![Version](https://img.shields.io/badge/version-0.2.0-brightgreen)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

> Bot Discord personnel propulsé par l'API Claude (Anthropic). Projet d'apprentissag
e d'une stack professionnelle complète : bot, tests, Docker, CI/CD GitHub Actions, d
éploiement Azure.

[English summary below ↓](#english-summary)

---

## Fonctionnalités

- Répond aux mentions (`@bot ta question`) en appelant Claude (Anthropic API)
- Gestion des erreurs API avec messages utilisateur en français (rate limit, connexi
on, erreur serveur)
- Retry automatique (3 tentatives) et timeout de 30 s côté client
- Prêt pour la production : Docker multi-stage, utilisateur non-root, restart automa
tique

---

## Quick Start — Docker Compose

```bash
# 1. Copier les variables d'environnement
cp .env.example .env
# Remplir ANTHROPIC_API_KEY et DISCORD_BOT_TOKEN dans .env

# 2. Lancer le bot
docker compose up -d

# 3. Consulter les logs
docker compose logs -f bot
```

---

## Variables d'environnement

| Variable | Obligatoire | Défaut | Description |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | ✅ | — | Clé API Anthropic |
| `DISCORD_BOT_TOKEN` | ✅ | — | Token du bot Discord |
| `CLAUDE_MODEL` | ❌ | `claude-haiku-4-5-20251001` | Modèle Claude utilisé |

Copier `.env.example` en `.env` et remplir les valeurs. Le fichier `.env` est ignoré
 par git.

---

## Stack technique

| Composant | Technologie |
|---|---|
| Langage | Python 3.10 / 3.11 / 3.12 |
| Bot Discord | discord.py ≥ 2.3 |
| LLM | Anthropic SDK ≥ 0.40 |
| Build | hatchling (`pyproject.toml`) |
| Tests | pytest + pytest-asyncio + pytest-cov |
| Linter / Formatter | ruff (règles E/F/I, ligne max 88) |
| Commits | commitizen (Conventional Commits) |
| Hooks pré-commit | pre-commit (ruff, trailing-whitespace, commitizen) |
| CI | GitHub Actions — lint + tests Python 3.10/3.11/3.12 |
| Conteneurisation | Docker multi-stage (builder → runtime) |
| Déploiement | Azure |

---

## Architecture

```
src/claude_discord_bot/
├── config.py         # Config (frozen dataclass) — lit ANTHROPIC_API_KEY & DISCORD_
BOT_TOKEN
├── claude_client.py  # ClaudeClient — wrapper Anthropic SDK avec gestion d'erreurs
└── bot.py            # Entrée Discord — écoute les mentions, appelle ClaudeClient
tests/
└── test_claude_client.py  # Tests unitaires (mock Anthropic)
```

**Flux de données :**
```
Discord mention → bot.py → ClaudeClient.ask() → Anthropic API → réponse Discord
```

**`Config`** est un dataclass `frozen=True` (immuable après création). Il échoue ave
c `RuntimeError` au démarrage si `ANTHROPIC_API_KEY` ou `DISCORD_BOT_TOKEN` est abse
nt — la mauvaise configuration est détectée tôt, pas au premier usage.

**`ClaudeClient`** retourne des chaînes d'erreur en français plutôt que de propager
des exceptions. Le bot Discord ne crashe jamais sur une erreur API.

---

## Commandes de développement

```bash
# Installation (première fois)
python -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install

# Tests
pytest                             # tous les tests + rapport de couverture
pytest tests/test_claude_client.py # un seul fichier
pytest -k "test_ask"               # un seul test par nom

# Lint & format
ruff check .                       # vérifier
ruff check . --fix                 # corriger automatiquement
ruff format .                      # formater

# Commit (Conventional Commits imposé)
cz commit
```

---

## Conformité EU AI Act & RGPD

### EU AI Act — Article 52 (transparence)

Ce bot respecte l'obligation de divulgation de l'Article 52 : les utilisateurs sont
informés qu'ils interagissent avec une IA. Le prompt système indique explicitement `
"Tu es un bot Discord"` et chaque réponse est signée, rendant la nature IA du bot tr
ansparente.

> *Les systèmes d'IA destinés à interagir avec des personnes physiques doivent infor
mer ces personnes qu'elles interagissent avec un système d'IA.* — EU AI Act, Art. 52
(1)

### RGPD

- **Pas de stockage persistant** : les messages Discord ne sont pas conservés après
traitement.
- **Sous-traitant tiers** : les messages envoyés à l'API Anthropic sont soumis à la
[politique de confidentialité d'Anthropic](https://www.anthropic.com/privacy). Les u
tilisateurs de ce bot doivent en être informés.
- **Journalisation minimale** : seules les erreurs techniques sont loggées — le cont
enu des messages n'est jamais enregistré.

---

## Liens

- **GitHub :** [nathansenglong/claude_discord_bot](https://github.com/nathansenglong
/claude_discord_bot)
- **Changelog :** [CHANGELOG.md](CHANGELOG.md)
- **Documentation Anthropic :** [docs.anthropic.com](https://docs.anthropic.com)
- **discord.py :** [discordpy.readthedocs.io](https://discordpy.readthedocs.io)

---

## English summary

Personal learning project — a Discord bot powered by the Anthropic Claude API, built
 with Python. Designed to practice a professional end-to-end stack: bot logic, autom
ated tests, Docker containerisation, GitHub Actions CI/CD, and Azure deployment.

**How it works:** Mention the bot in any Discord channel with a question. It calls C
laude via the Anthropic API and replies with the response (capped at 2 000 character
s). API errors are caught and returned as friendly French messages; the bot never cr
ashes on API failures.

**EU AI Act compliance:** The system prompt explicitly identifies the bot as an AI s
ystem (Art. 52 transparency requirement).
