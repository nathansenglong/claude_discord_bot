# claude-discord-bot

[![CI](https://github.com/nathansenglong/claude_discord_bot/actions/workflows/ci.yml/badge.svg)](https://github.com/nathansenglong/claude_discord_bot/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue)
![Version](https://img.shields.io/badge/version-0.2.0-brightgreen)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

> Bot Discord personnel propulsé par l'API Claude (Anthropic). Projet d'apprentissage d'une stack professionnelle complète : bot, tests automatisés, Docker, CI/CD GitHub Actions, déploiement Azure, workflow Git pro (branches, PR, Conventional Commits).

[English summary below ↓](#english-summary)

---

## Fonctionnalités

- Répond aux mentions (`@bot ta question`) en appelant Claude (API Anthropic)
- Gestion des erreurs API avec messages utilisateur en français (rate limit, connexion, erreur serveur)
- Retry automatique (3 tentatives) et timeout de 30 s côté client
- Prêt pour la production : Docker multi-stage, utilisateur non-root, redémarrage automatique

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

Copier `.env.example` en `.env` et remplir les valeurs. Le fichier `.env` est ignoré par git.

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
├── config.py         # Config (frozen dataclass) — lit ANTHROPIC_API_KEY & DISCORD_BOT_TOKEN
├── claude_client.py  # ClaudeClient — wrapper Anthropic SDK avec gestion d'erreurs
└── bot.py            # Entrée Discord — écoute les mentions, appelle ClaudeClient
tests/
└── test_claude_client.py  # Tests unitaires (mock Anthropic)
```

**Flux de données :**

```
Discord mention → bot.py → ClaudeClient.ask() → Anthropic API → réponse Discord
```

**`Config`** est un dataclass `frozen=True` (immuable après création). Il échoue avec `RuntimeError` au démarrage si `ANTHROPIC_API_KEY` ou `DISCORD_BOT_TOKEN` est absent : la mauvaise configuration est détectée tôt, pas au premier usage.

**`ClaudeClient`** retourne des chaînes d'erreur en français plutôt que de propager des exceptions. Le bot Discord ne crashe jamais sur une erreur API.

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

### EU AI Act — Article 50 (transparence)

Le règlement (UE) 2024/1689 impose aux fournisseurs de systèmes d'IA destinés à interagir directement avec des personnes physiques de veiller à ce que ces personnes soient informées qu'elles interagissent avec une IA (article 50, paragraphe 1). L'article 52 mentionné dans la version initiale de la proposition correspond désormais à cet article 50.

Pour satisfaire cette obligation, le bot signale sa nature IA **dans les messages visibles par les utilisateurs** (signature de chaque réponse). Le prompt système, lui, n'est pas visible des utilisateurs et ne suffit pas à lui seul.

### RGPD

- **Pas de stockage persistant** : les messages Discord ne sont pas conservés après traitement.
- **Sous-traitant tiers** : les messages envoyés à l'API Anthropic sont soumis à la [politique de confidentialité d'Anthropic](https://www.anthropic.com/privacy). Les utilisateurs de ce bot doivent en être informés.
- **Journalisation minimale** : seules les erreurs techniques sont loggées. Le contenu des messages n'est jamais enregistré.

---

## Liens

- **GitHub :** [nathansenglong/claude_discord_bot](https://github.com/nathansenglong/claude_discord_bot)
- **Changelog :** [CHANGELOG.md](CHANGELOG.md)
- **Documentation Anthropic :** [docs.anthropic.com](https://docs.anthropic.com)
- **discord.py :** [discordpy.readthedocs.io](https://discordpy.readthedocs.io)

---

## English summary

Personal learning project: a Discord bot powered by the Anthropic Claude API, built with Python. Designed to practice a professional end-to-end stack: bot logic, automated tests, Docker containerisation, GitHub Actions CI/CD, and Azure deployment.

**How it works:** Mention the bot in any Discord channel with a question. It calls Claude via the Anthropic API and replies with the response (capped at 2,000 characters). API errors are caught and returned as friendly French messages; the bot never crashes on API failures.

**EU AI Act compliance:** The bot discloses its AI nature in the messages users actually see (transparency obligation, Art. 50 of Regulation (EU) 2024/1689).
