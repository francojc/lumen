# Development Project Progress

**Project:** orbitr
**Status:** Active development - v0.3.0 planning in progress
**Last Updated:** 2026-04-17

## Current Status Overview

### Development Phase

- **Current Phase:** Phase 8 (v0.3.0 planning and reliability)
- **Phase Progress:** Phases 1-7 complete
- **Overall Project Progress:** v0.1.x and v0.2.0 shipped; roadmap reset in progress

### Recent Accomplishments

- Phase 7 complete: Zotero `list/get/search/export-md` shipped with tests
- `v0.2.0` tagged and released
- README and release docs updated for new Zotero command surface
- Release automation improved (`just release`)
- Test suite expanded to 410 passing tests

## Milestone Tracking

### Completed Milestones

- [x] Phase 1: Architecture and scaffolding
- [x] Phase 2: Core data layer
- [x] Phase 3: Command implementation
- [x] Phase 4: Display and polish
- [x] Phase 5: Testing and documentation
- [x] Phase 6: Initial release
- [x] Phase 7: Zotero library enhancements
- [x] v0.2.0 release tag

### Active Milestones (Phase 8)

- [ ] Milestone 8.1 - v0.3 scope and acceptance criteria, including Zotero recent-entry UX decision (target: 2026-04-24)
- [ ] Milestone 8.2 - coverage baseline and CI gate (target: 2026-05-01)
- [ ] Milestone 8.3 - API reliability + Google Scholar v1.1 feasibility slice (target: 2026-05-15)
- [ ] Milestone 8.4 - documentation and status cadence reset + CI consistency guardrail (target: 2026-05-22)

### At-Risk Milestones

- **Potential risk:** v0.3 scope remains undefined, which can delay implementation start
- **Potential risk:** Google Scholar feasibility may fail reliability criteria

## Build and Test Status

### Build Health

- **Last Confirmed Healthy Run:** 2026-04-08 (`pytest`, `ruff`, `pyright`)
- **Warnings:** None currently tracked

### Test Status

- **Tests Passing:** 410
- **Coverage Tracking:** Not yet enforced in CI (planned in Milestone 8.2)
- **Open Defects:** No active critical/high defects recorded

## Current Work

### Active Focus

- Finalize v0.3 scope and sequencing
- Add measurable quality gate via coverage in CI
- Establish lightweight operational logging cadence (`logs/`)
- Decide and scope Zotero recently-added workflow (`zotero recent` vs extending `zotero search`)
- Define and implement docs consistency guardrails in CI
- Strengthen API failure handling and health-check depth

### Open Tasks (next 2 weeks)

- [ ] Publish v0.3 milestone issue list with owners and acceptance criteria
- [ ] Decide Zotero recently-added command design and write command-level acceptance tests
- [ ] Add `pytest-cov` and set an initial CI threshold
- [ ] Add docs consistency check in CI for planning/progress phase and version fields
- [ ] Verify graceful error exits for API/query failures and add missing test coverage

### Blockers

- None currently identified

## Verification Notes (2026-04-17)

- `zotero search` is currently query-based and does not support date-added filters.
- Current code supports sorting in `zotero list`, but accepted sort values exclude `dateAdded`.
- `doctor` currently verifies endpoint reachability, but it does not perform semantic payload checks.
- Search/query command paths already use `SourceError` with user-facing suggestions.
- Zotero client methods do not yet consistently map backend/network exceptions into `SourceError`/`LumenError`; this is a v0.3 reliability task.

## Deferred Items

- Group library support in Zotero (v2)
- PDF text extraction/full-text indexing (v2)
- Custom Jinja templates for `zotero export-md` (v2)
- Batch `export-md` workflow enhancements (v2)
- CLI-based Zotero item editing/update support (v2)

## Release Outlook

### Next Release

- **Version:** v0.3.0 (planning stage)
- **Target Window:** TBD after Milestone 8.1
- **Candidate Themes:** reliability, coverage discipline, optional Google Scholar feasibility outcome

### Release History

| Version | Date | Key Changes |
|---|---|---|
| 0.2.0 | 2026-04-08 | Zotero `list/get/search/export-md`, command and docs expansion |
| 0.1.1 | 2026-04-06 | Stabilization patch after initial release |
