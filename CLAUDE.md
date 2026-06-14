# AlgaeCal AI Agents — CLAUDE.md

## Project
Portfolio of 6 AI agents acting as a digital workforce for AlgaeCal (~100-person DTC health supplements company, Vancouver).

## Conventions
- Python 3.11+, no unnecessary dependencies
- LLM calls go through `shared/llm/provider.py` — never call APIs directly
- Each agent lives in `agents/<name>/` with its own README
- Mock data in `shared/data/` uses SQLite — realistic AlgaeCal-like data
- Environment variables in `.env` (git-ignored), template in `.env.example`

## Code Style
- Simple > clever. Minimal abstractions.
- No docstrings on obvious functions. Comments only where logic isn't self-evident.
- Keep agents self-contained — each should run independently.

## Git
- Commit messages: imperative mood, concise, explain the "why"
- Never commit `.env` or API keys
