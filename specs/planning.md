# Development Project Planning

**Project:** orbitr
**Status:** Active development - v0.3.0 planning
**Last Updated:** 2026-04-17

## Project Overview

### Software Description

- **Application Type:** CLI tool
- **Target Platform:** macOS and Linux (cross-platform)
- **Primary Language:** Python >= 3.10
- **Key Libraries/Frameworks:** Typer (CLI), Rich (terminal output), httpx (async HTTP), Pydantic (models), pyzotero (Zotero), feedparser (arXiv)

### Problem Statement

- Researchers, academics, and students need a fast, composable terminal workflow for literature discovery and reference management.
- Existing tools are often GUI-first, source-limited, or weak for automation.
- `orbitr` provides multi-source search, ranking, export, and Zotero integration with Unix-friendly JSON and piping.

### Goals and Non-Goals

#### Goals

- [x] Multi-source search (arXiv, Semantic Scholar) with intelligent deduplication and ranking
- [x] Advanced field-specific queries (title, author, abstract, venue, date range) via a single `search` command
- [x] Citation lookup, author search, and paper recommendations from seed titles
- [x] Bibliography export to BibTeX, RIS, and CSL-JSON
- [x] Zotero library integration: add papers, create/list collections, browse/search items, export items as markdown
- [x] Local result caching with TTL tiers for search, paper, and citation data
- [x] Full Unix composability: stdout/stderr discipline, JSON output, pipe-friendly design
- [x] Robust help system, informative errors with suggestions, and `orbitr doctor` diagnostics
- [x] Shell completions for Zsh, Bash, and Fish
- [x] `orbitr init` guided setup for credentials and defaults

#### Non-Goals

- No GUI or TUI - terminal output only
- No PDF download or full-text retrieval
- No built-in AI summarization or annotation
- No Zotero group library support in v1/v0.2
- No PDF text extraction or full-text indexing
- No custom Jinja templates for `zotero export-md` in v0.2
- No support for databases beyond arXiv and Semantic Scholar in v0.2 (Google Scholar deferred)
- No multi-user or server mode

## Timeline and Milestones

### Phase 1: Architecture and Scaffolding - COMPLETE

- [x] Initialize repo and packaging scaffold
- [x] Typer skeleton with global flags
- [x] Config resolution layer
- [x] Command stubs
- [x] `orbitr init` and `orbitr doctor` skeletons

### Phase 2: Core Data Layer - COMPLETE

- [x] Pydantic models (`Paper`, `Author`, `SearchResult`)
- [x] arXiv client
- [x] Semantic Scholar client
- [x] Deduplication and ranking
- [x] SQLite cache with TTL tiers
- [ ] Google Scholar client (deferred)

### Phase 3: Command Implementation - COMPLETE

- [x] `search`, `paper`, `cite`, `author`, `recommend`
- [x] `export`, `query`, `cache`, `init`, `doctor`
- [x] `zotero add/collections/new`

### Phase 4: Display and Polish - COMPLETE

- [x] Table/list/detail/json renderers
- [x] TTY format auto-selection
- [x] Pager integration
- [x] Error polish and consistency

### Phase 5: Testing and Documentation - COMPLETE

- [x] Expanded unit/integration tests
- [x] CI pipeline
- [x] README and setup docs
- [x] Smoke test script

### Phase 6: Initial Release - COMPLETE

- [x] Build artifacts verified
- [x] v0.1.x release/tag complete

### Phase 7: Zotero Library Enhancements - COMPLETE

- [x] `ZoteroClient.list_items()`
- [x] `ZoteroClient.get_item()`
- [x] `ZoteroClient.search_items()`
- [x] `orbitr zotero list`
- [x] `orbitr zotero get <item_key>`
- [x] `orbitr zotero search <query>`
- [x] `orbitr zotero export-md <item_key>`
- [x] `--format keys` support on list/search
- [x] Tests for new client methods and subcommands
- [x] v0.2.0 release and tag

### Phase 8: v0.3.0 Planning and Reliability - ACTIVE

#### Milestone 8.1 - Scope and acceptance criteria (target: 2026-04-24)

- [ ] Define v0.3.0 feature scope (must-have / should-have / defer)
- [ ] Define acceptance criteria per feature
- [ ] Publish milestone issue list

#### Milestone 8.2 - Coverage baseline and CI gate (target: 2026-05-01)

- [ ] Add `pytest-cov` config and baseline coverage report
- [ ] Add minimum coverage threshold in CI
- [ ] Document local coverage workflow in README/justfile

#### Milestone 8.3 - Google Scholar v1.1 feasibility slice (target: 2026-05-15)

- [ ] Prototype best-effort client behind feature flag
- [ ] Add fixture-driven tests for parser stability
- [ ] Decide ship/defer based on reliability criteria

#### Milestone 8.4 - Documentation and status operations (target: 2026-05-22)

- [ ] Keep `specs/planning.md` and `specs/progress.md` synchronized weekly
- [ ] Reintroduce `logs/` weekly and session status cadence
- [ ] Add release checklist updates for post-v0.2 workflow

## Risks and Constraints

### Technical Risks

- Google Scholar scraping fragility
- Semantic Scholar rate limiting when no API key is configured
- Async command complexity in Typer command boundaries

### Scope Risks

- Recommendation quality can trigger scope creep
- Zotero edge cases (group libraries, linked attachments) remain deferred

## Success Metrics (v0.3 planning window)

### Delivery Metrics

- [ ] v0.3.0 milestones and dates approved
- [ ] All v0.3.0 must-have features mapped to issues

### Quality Metrics

- [ ] CI includes coverage report and threshold gate
- [ ] No regression in existing command help, error handling, or output contracts

### Operational Metrics

- [ ] Weekly status entry added under `logs/`
- [ ] Session notes captured for major implementation blocks
