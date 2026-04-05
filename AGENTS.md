# lumen — Agent Project Context

## Software Purpose

`lumen` is a Python CLI tool for academic literature search and reference management. It queries arXiv, Semantic Scholar, and Google Scholar concurrently, deduplicates and ranks results, and integrates with the Zotero reference manager. Target users: researchers, academics, and students who prefer terminal-based workflows.

## Architecture Overview

CLI pipeline: command dispatch → concurrent async API clients → core processing (dedup, ranking, cache) → display layer (Rich or JSON).

**Key components:**

- `src/lumen/cli.py` — Typer root app; global flags; injects config into context
- `src/lumen/config.py` — layered config: CLI flags > env vars > `~/.config/lumen/config.toml` > defaults
- `src/lumen/commands/` — one module per command (`search`, `paper`, `cite`, `author`, `recommend`, `export`, `query`, `zotero`, `cache`, `init`, `doctor`)
- `src/lumen/clients/` — async httpx clients: `arxiv.py`, `semantic_scholar.py`; all extend `base.py` (retry, rate limiting, circuit break); Google Scholar deferred to v1.1
- `src/lumen/core/` — `models.py` (Pydantic), `deduplication.py`, `ranking.py`, `cache.py` (SQLite), `export.py` (BibTeX/RIS/CSL-JSON)
- `src/lumen/zotero/client.py` — pyzotero wrapper
- `src/lumen/display/` — `table.py`, `list.py`, `detail.py`, `json_fmt.py`

## Build, Test, and Run

```bash
# Dev install
uv sync
uv tool install --editable .

# Run without installing
uv run lumen --help

# Build wheel
uv build

# Lint and format
ruff check src/ tests/
ruff format src/ tests/

# Type check
pyright src/

# Tests
uv run pytest                                          # all tests
uv run pytest tests/ -m "not integration"             # unit only
uv run pytest --cov=src/lumen --cov-report=term-missing  # with coverage
```

## Language and Stack

- **Python** ≥ 3.10; `uv` for deps and packaging; `hatchling` build backend
- **CLI:** Typer + Click
- **Terminal output:** Rich
- **HTTP:** httpx (async)
- **Models:** Pydantic v2
- **Cache:** SQLite (stdlib `sqlite3`)
- **Zotero:** pyzotero
- **Code style:** `ruff format` (88 chars), `ruff check` (rules: E, F, UP, B, SIM, I), `pyright` basic

## Directory Structure

```
lumen/
├── pyproject.toml
├── flake.nix
├── CLAUDE.md
├── README.md
├── .env.example
├── specs/               # planning.md, progress.md, implementation.md
├── logs/                # session and weekly review logs
├── src/lumen/           # source package
├── tests/               # pytest suite + fixtures/
└── .gitignore
```

## Development Workflow

- Conventional commits: `type(scope): message` (feat, fix, chore, docs, test, refactor)
- All commands must have complete `--help` text with a usage example before merging
- Errors go to stderr; data goes to stdout — enforce at every command boundary
- All new commands: add entry to `cli.py`, stub in `commands/`, unit test in `tests/test_<command>.py`
- Check `specs/planning.md` for the current phase and open tasks
- Update `specs/progress.md` after completing a milestone or feature

## Key Conventions

- **Exit codes:** 0 success, 1 general error, 2 usage error, 3 config error, 4 no results
- **Config path:** `~/.config/lumen/config.toml` (XDG); cache at `~/.cache/lumen/`
- **Credentials file permissions:** `0600` — enforced in `lumen init`
- **TTY detection:** when stdout is not a TTY, default `--format` to `json` automatically
- **`NO_COLOR`** env var disables all Rich color; `--no-color` flag does the same
- **Async in Typer:** wrap async work in `asyncio.run()` at the command level; no persistent event loop
- **Google Scholar:** deferred to v1.1 — do not implement in v1
- **Deduplication threshold:** 85% fuzzy title similarity (configurable internally)

## How to Use Claude Effectively Here

- **Before implementing a command:** read `specs/implementation.md` for the module structure and key interfaces; check `specs/progress.md` for current status
- **Error messages:** always include what failed, why, and a fix suggestion — see `specs/implementation.md` § Error Handling for the pattern
- **Adding a new command:** follow the pattern in existing `commands/` modules; register in `cli.py`; add `--help` text with a real example
- **Tests:** use `tests/fixtures/` for API responses; mock with `respx`; never make live API calls in tests
- **Display:** add new renderers in `display/`; always accept `format: Literal["table","list","detail","json"]` and honor `NO_COLOR`
