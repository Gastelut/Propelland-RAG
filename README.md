# Propelland Internal RAG (Local Dropbox Knowledge System)

Local, private RAG system for Propelland’s Dropbox folders.

It:
- crawls selected Dropbox folders
- stores file metadata + crawl status in SQLite
- detects proposal-like PDFs by folder name
- creates structured “project cards” via OpenAI
- stores project-card embeddings in Qdrant for semantic search
- answers questions using retrieved project cards + sources

---

## Folder layout (recommended)

### Code (Git repo)
`C:\Users\Bastian\propelland-rag\`
- `crawl_propelland.py`
- `search_projects.py`
- `answer_projects.py`
- `find_files.py`
- helper scripts (optional)

### Data (NOT in Git)
`C:\Users\Bastian\propelland-rag-data\`
- `db\rag_state.sqlite`
- `qdrant\` (Qdrant storage)
- optional `logs\`

---

## Prereqs

- Windows + Python 3.x
- Docker Desktop
- Qdrant container running locally
- OpenAI API key (stored in `.env`, not committed)

---

## Qdrant (Docker) — run with persistent storage

One-line run (stores data in the dedicated data folder):

```powershell
docker run -d --name qdrant -p 6333:6333 -v C:\Users\Bastian\propelland-rag-data\qdrant:/qdrant/storage qdrant/qdrant:latest





TIPS:


Now here’s a ready-to-drop **README.md** for your new repo (`C:\Users\Bastian\propelland-rag\`).

````md
# Propelland Internal RAG (Local Dropbox Knowledge System)

Local, private RAG system for Propelland’s Dropbox folders.

It:
- crawls selected Dropbox folders
- stores file metadata + crawl status in SQLite
- detects proposal-like PDFs by folder name
- creates structured “project cards” via OpenAI
- stores project-card embeddings in Qdrant for semantic search
- answers questions using retrieved project cards + sources

---

## Folder layout (recommended)

### Code (Git repo)
`C:\Users\Bastian\propelland-rag\`
- `crawl_propelland.py`
- `search_projects.py`
- `answer_projects.py`
- `find_files.py`
- helper scripts (optional)

### Data (NOT in Git)
`C:\Users\Bastian\propelland-rag-data\`
- `db\rag_state.sqlite`
- `qdrant\` (Qdrant storage)
- optional `logs\`

---

## Prereqs

- Windows + Python 3.x
- Docker Desktop
- Qdrant container running locally
- OpenAI API key (stored in `.env`, not committed)

---

## Qdrant (Docker) — run with persistent storage

One-line run (stores data in the dedicated data folder):

```powershell
docker run -d --name qdrant -p 6333:6333 -v C:\Users\Bastian\propelland-rag-data\qdrant:/qdrant/storage qdrant/qdrant:latest
````

Verify:

```powershell
curl.exe http://localhost:6333/collections
```

---

## Configuration

### SQLite DB path

In your scripts (e.g. `crawl_propelland.py`) set:

```python
DB_PATH = r"C:\Users\Bastian\propelland-rag-data\db\rag_state.sqlite"
```

### Dropbox roots to crawl

In `crawl_propelland.py`, edit `ROOTS` to your local Dropbox sync paths, e.g.:

* `...\Propelland Dropbox\01 Client Projects`
* `...\Propelland Dropbox\02 Business Development`

(You can add/remove roots as needed.)

### Proposal detection

A PDF is considered “proposal-like” if its **path** contains:

* `proposal`, `proposals`, `propuesta`, `propuestas`, `pitch` (case-insensitive)

Only those PDFs trigger **project card generation**.

---

## Install Python deps

Create a venv (recommended) and install:

```powershell
py -m venv .venv
.\.venv\Scripts\activate
py -m pip install -r requirements.txt
```

Minimal `requirements.txt` typically includes:

* `openai`
* `qdrant-client`
* `pypdf`
* `python-dotenv`

---

## Run

### 1) Crawl + index

Scans roots, stores metadata in SQLite, extracts PDF text when needed, creates project cards, and writes embeddings to Qdrant.

```powershell
py .\crawl_propelland.py
```

### 2) Keyword file search (SQLite)

Searches file paths + project fields:

```powershell
py .\find_files.py "melia proposal"
```

### 3) Semantic search (Qdrant)

Searches project cards semantically:

```powershell
py .\search_projects.py "VOC strategy in hospitality"
```

### 4) Ask questions (RAG answer)

Retrieves relevant project cards from Qdrant, then answers with sources:

```powershell
py .\answer_projects.py "List projects related to CRM or Salesforce"
```

---

## Incremental crawling (important)

Crawler uses a `content_sig` (hash of file size + mtime_ns) to skip unchanged files.
On repeated runs, it should show high `skipped_unchanged` and near-zero reprocessing.

---

## Notes on Dropbox “online-only”

Dropbox Smart Sync may hydrate files on demand when the crawler reads them.
Metadata scanning does not download full content; reading PDFs can trigger download.

---

## What NOT to commit

Do not commit:

* `.env` (API keys)
* SQLite DB (`*.sqlite`)
* Qdrant storage folder (`propelland-rag-data/qdrant`)
* any Dropbox content

Use `.gitignore` to enforce this.

Example `.gitignore`:

```gitignore
.env
*.sqlite
*.sqlite*
__pycache__/
*.log

# runtime data folder
propelland-rag-data/
rag_db/
qdrant_data/
```

---

## Quick health checks

```powershell
curl.exe http://localhost:6333/collections
py .\answer_projects.py "List projects related to CRM"
```

```

If you want, paste your current file list in `C:\Users\Bastian\propelland-rag\` and I’ll tell you exactly what to keep vs move into `propelland-rag-data\`.
```
