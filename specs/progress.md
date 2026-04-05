# Development Project Progress

**Project:** lumen
**Status:** Planning
**Last Updated:** 2026-04-05

## Current Status Overview

### Development Phase

- **Current Phase:** Architecture & Design
- **Phase Progress:** 5% complete
- **Overall Project Progress:** 5% complete

### Recent Accomplishments

- README written and refined — 2026-04-05
- Project structure and command surface designed — 2026-04-05
- specs/ scaffolded with planning, progress, and implementation docs — 2026-04-05

### Active Work

- [ ] Initialize repo and `pyproject.toml` — target 2026-04-12
- [ ] Typer app skeleton with global flags — target 2026-04-12
- [ ] Config resolution layer — target 2026-04-14

## Milestone Tracking

### Completed Milestones

- [x] ~~README and project design~~ — 2026-04-05

### Upcoming Milestones

- [ ] Phase 1 complete: repo scaffolded, Typer skeleton, config layer — target 2026-04-14
- [ ] Phase 2 complete: all three API clients + dedup/ranking/cache — target 2026-04-28
- [ ] Phase 3 complete: all 11 commands implemented — target 2026-05-26
- [ ] Phase 4 complete: display layer polished, errors finalized — target 2026-06-09
- [ ] v0.1.0 release — target 2026-06-23

### At-Risk Milestones

_None identified yet._

## Build and Test Status

### Build Health

- **Last Successful Build:** N/A (not yet scaffolded)
- **Build Time:** N/A
- **Build Warnings:** N/A

### Test Results

- **Unit Tests:** N/A
- **Integration Tests:** N/A
- **Test Coverage:** N/A

### Open Defects

- **Critical:** 0
- **High:** 0
- **Medium:** 0
- **Low:** 0

## Feature Progress

### Completed Features

_None yet._

### In Progress

- [ ] Project scaffolding — 0% complete

### Planned

- [ ] `lumen search` — Phase 3
- [ ] `lumen paper` — Phase 3
- [ ] `lumen cite` — Phase 3
- [ ] `lumen author` — Phase 3
- [ ] `lumen recommend` — Phase 3
- [ ] `lumen export` — Phase 3
- [ ] `lumen query` — Phase 3
- [ ] `lumen zotero add/collections/new` — Phase 3
- [ ] `lumen cache stats/clean/clear` — Phase 3
- [ ] `lumen init` — Phase 3
- [ ] `lumen doctor` — Phase 3
- [ ] Rich display layer (table, list, detail, JSON) — Phase 4
- [ ] Shell completions (Zsh, Bash, Fish) — Phase 4

### Deferred or Cut

_Nothing deferred yet._

## Technical Debt

### Known Debt

_None accumulated yet — project not started._

## Dependency Status

### External Dependencies

| Package | Version | Status |
|---|---|---|
| `typer` | latest stable | Planned |
| `rich` | latest stable | Planned |
| `httpx` | latest stable | Planned |
| `pydantic` | ≥ 2.0 | Planned |
| `pyzotero` | latest stable | Planned |
| `feedparser` | latest stable | Planned |
| `python-dateutil` | latest stable | Planned |
| `beautifulsoup4` | latest stable | Planned |
| `python-dotenv` | latest stable | Planned |

## Challenges and Blockers

### Current Blockers

_None._

### Resolved Challenges

_None yet._

### Lessons Learned

- Google Scholar client should be designed as best-effort from the start to avoid over-engineering a fragile scraper

## Next Steps

### Immediate Actions (Next 2 Weeks)

- [ ] Create `pyproject.toml` with Hatchling build backend and all dependencies declared
- [ ] Initialize git repo and push to GitHub
- [ ] Create `src/lumen/` package skeleton: `cli.py`, `config.py`, stub `commands/`
- [ ] Implement global flag handling (`--version`, `--verbose`, `--quiet`, `--no-color`, `--config`)
- [ ] Implement config file loading with XDG path defaults

### Medium-term Goals (Next Month)

- [ ] All three API clients implemented with basic search working
- [ ] Deduplication and ranking operational
- [ ] SQLite cache layer in place
- [ ] `lumen search` end-to-end for at least arXiv + Semantic Scholar

### Decisions Needed

- ~~**Async strategy in Typer:**~~ resolved — Option A (`asyncio.run()` per command, `asyncio.gather()` across sources inside async impl); see implementation.md decision log
- ~~**Google Scholar inclusion in v1:**~~ resolved — deferred to v1.1

## Release Planning

### Next Release

- **Version:** 0.1.0
- **Target Date:** 2026-06-23
- **Included Features:** All 11 commands, three sources, Zotero integration, caching, shell completions, `lumen init`, `lumen doctor`
- **Release Blockers:** Everything — not yet started

### Release History

| Version | Date | Key Changes |
|---|---|---|
| — | — | — |
