# orbitr Zotero extensions for LLM Wiki

Work order for expanding `orbitr zotero` subcommands to support the LLM Wiki ingestion pipeline and general library management from the CLI.

**Codebase:** `~/.local/cli/orbitr/`
**Framework:** Python / Typer CLI / pyzotero / Pydantic models

## Current state

| Feature | Status |
|---|---|
| `zotero add <paper_id>` | ✅ Works (fetches from arXiv/S2, creates Zotero item) |
| `zotero collections` | ✅ Works (lists all collections) |
| `zotero new <name>` | ✅ Works (creates collection) |
| `zotero list` | ❌ Missing |
| `zotero get` | ❌ Missing |
| `zotero search` | ❌ Missing |
| `zotero export-md` | ❌ Missing |
| Semantic Scholar API key | ✅ Already configured (`orbitr doctor` confirms) |

## Implementation order

```
1. zotero list      (foundation – browse what's there)
2. zotero get       (deep dive – pull full details)
3. zotero search    (discoverability – find items by keyword)
4. zotero export-md (pipeline – markdown for wiki-ingest)
```

Each item is independently useful and testable. Items 1–3 are pure read operations (no risk to library data). Item 4 only writes to the local filesystem.

---

## 1. `zotero list` – list items in a collection

**Files:** `zotero/client.py` (new method), `commands/zotero.py` (new command)

### Client method – `ZoteroClient.list_items()`

- Parameters: `collection_key: str | None`, `limit: int = 25`, `sort: str = "dateModified"`, `direction: str = "desc"`, `item_type: str | None = None`
- Calls `self._zot.collection_items(collection_key, ...)` when a collection is given, otherwise `self._zot.items(...)`
- Returns `list[dict]` (raw Zotero item dicts)
- Must handle pagination internally when `limit > 100` (Zotero API max per request)

### CLI command – `orbitr zotero list`

- Options:
  - `--collection/-c` (name or key)
  - `--limit/-n` (default 25)
  - `--sort` (dateModified, title, date)
  - `--format/-f` (table, json, keys)
- Table columns: `Key`, `Title` (truncated 60 chars), `Authors` (first author + "et al."), `Year`, `Type`
- `--format keys` outputs bare item keys one-per-line (pipeable to `xargs -I{} orbitr zotero get {}`)

### Examples

```bash
orbitr zotero list -c "ed-ai" -n 50
orbitr zotero list -c "ed-ai" --format keys | xargs -I{} orbitr zotero get {}
orbitr zotero list --sort title --format json
```

### Rationale

The wiki-ingest pipeline needs to browse Zotero collections to find ingestion candidates. Currently there is no way to see what's in a collection without opening the Zotero GUI.

---

## 2. `zotero get` – fetch full item details

**Files:** `zotero/client.py` (new method), `commands/zotero.py` (new command)

### Client method – `ZoteroClient.get_item()`

- Parameter: `item_key: str`
- Calls `self._zot.item(item_key)` for metadata
- Calls `self._zot.children(item_key)` for attachments and notes
- Returns structured dict:

```python
{
    "meta": { ... },            # full Zotero item data
    "notes": ["note text", ...],
    "attachments": [
        {"filename": "...", "path": "...", "content_type": "..."},
        ...
    ]
}
```

### CLI command – `orbitr zotero get <item_key>`

- Options:
  - `--format/-f` (detail, json)
  - `--notes/--no-notes` (default: include notes)
- `detail` format: Rich panel with title, authors, abstract, venue, year, DOI, URL, tags, collections, then notes as indented blocks
- `json` format: full structured dict to stdout
- Reports local PDF path if an attachment with `content_type=application/pdf` exists

### Examples

```bash
orbitr zotero get ABCD1234
orbitr zotero get ABCD1234 --format json
orbitr zotero get ABCD1234 --no-notes
```

### Rationale

`wiki-ingest` needs to pull full metadata + abstract + notes for a Zotero item to build a source summary page. `orbitr paper` only queries arXiv/S2, not the local Zotero library.

---

## 3. `zotero search` – search within the Zotero library

**Files:** `zotero/client.py` (new method), `commands/zotero.py` (new command)

Not in the original WORKLIST but high value. Currently there is no way to search the local library from the CLI.

### Client method – `ZoteroClient.search_items()`

- Parameters: `query: str`, `collection_key: str | None = None`, `limit: int = 25`
- Calls `self._zot.items(q=query, ...)` (pyzotero supports the `q` parameter for full-text search)
- When `collection_key` is set, scopes to that collection

### CLI command – `orbitr zotero search <query>`

- Options: `--collection/-c`, `--limit/-n`, `--format/-f` (table, json, keys)
- Same table format as `zotero list`

### Examples

```bash
orbitr zotero search "language learning"
orbitr zotero search "transformer" -c "LLMs-as-ling-tools" --format keys
```

### Rationale

With 100+ items across collections, CLI search is needed to find items for ingestion or citation without switching to the GUI. Critical for the `research-search` skill which currently can only search external APIs.

---

## 4. `zotero export-md` – export item as markdown source file

**Files:** `zotero/client.py` (optional utility), `commands/zotero.py` (new command)

### CLI command – `orbitr zotero export-md <item_key>`

- Options:
  - `--output/-o` (output path; default: stdout)
  - `--template` (future: custom Jinja template, not implemented in v1)
- When `--output` is a directory, auto-generates filename: `YYYY-Author-Short-Title.md`

### Output format

```markdown
---
title: "Paper Title"
authors: [Author One, Author Two]
year: 2024
doi: "10.xxxx/yyyy"
zotero_key: ITEM_KEY
zotero_url: "zotero://select/items/0_ITEM_KEY"
tags: [tag1, tag2]
type: source
---

# Paper Title

**Authors:** Author One, Author Two
**Year:** 2024 | **Venue:** Journal Name
**DOI:** [10.xxxx/yyyy](https://doi.org/10.xxxx/yyyy)

## Abstract

Abstract text here.

## Notes

Zotero note content here (if any).
```

### Examples

```bash
orbitr zotero export-md ABCD1234
orbitr zotero export-md ABCD1234 -o kb/sources/raw/
orbitr zotero list -c "ed-ai" --format keys | xargs -I{} orbitr zotero export-md {} -o kb/sources/raw/
```

### Rationale

Completes the ingestion pipeline: `orbitr zotero export-md <key> → wiki-ingest`. Gives the wiki-ingest skill a clean markdown file with frontmatter it can parse, rather than requiring it to call `zotero get` and assemble metadata itself.

---

## Cross-cutting concerns

| Item | Detail |
|---|---|
| Error handling | All new commands follow the existing `ConfigError`/`OrbitrError`/`SourceError` pattern in `zotero_add` |
| `--format keys` | All list/search commands support `keys` format for piping |
| Pagination | `list` and `search` handle pyzotero's built-in pagination when `limit > 100` (Zotero API cap per request) |
| Help text | Update the `zotero` Typer app help string to reflect new subcommands |

---

## Out of scope (defer to v2)

- Group library support (hardcoded to `"user"` library type in `ZoteroClient`)
- PDF text extraction / full-text indexing
- Batch `export-md` for entire collections (composable via `list --format keys | xargs`)
- Zotero item editing/updating from CLI
- Custom Jinja templates for `export-md`
