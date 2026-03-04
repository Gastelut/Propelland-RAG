import os, sys, re, sqlite3, hashlib, datetime, logging
import warnings
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

# Suppress msvcrt import warning from portalocker (Windows specific)
warnings.filterwarnings("ignore", category=ImportWarning)

# Silence pypdf spam
logging.getLogger("pypdf").setLevel(logging.ERROR)

# ----- CONFIG -----
ROOTS = [
    r"C:\Users\Bastian\Propelland Dropbox\01 Client Projects",
    r"C:\Users\Bastian\Propelland Dropbox\02 Business Development",
]

DB_PATH = r"C:\Users\Bastian\propelland-rag-data\db\rag_state.sqlite"
QDRANT_URL = None  # Use local storage instead of Docker
QDRANT_PATH = r"C:\Users\Bastian\propelland-rag-data\qdrant"
PROJECT_COLLECTION = "project_cards"

CONTENT_EXTS = {".pdf"}
KEYNOTE_EXT = ".key"

PROPOSAL_DIR_MATCH = re.compile(r"(proposal|proposals|propuesta|propuestas|pitch)", re.IGNORECASE)

MAX_PDF_PAGES = 20
MAX_TEXT_CHARS = 12000
MAX_PDF_BYTES = 50 * 1024 * 1024  # 50MB

# ----- HELPERS -----
def now_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def is_online_only(path: str) -> bool:
    import os
    try:
        fd = os.open(path, os.O_RDONLY)
        os.close(fd)
        return False
    except Exception:
        return True

    
def calc_content_sig(size, mtime_ns) -> str | None:
    if size is None or mtime_ns is None:
        return None
    return hashlib.md5(f"{size}|{mtime_ns}".encode("utf-8")).hexdigest()

def file_id_for_path(path_str: str) -> str:
    return hashlib.md5(path_str.encode("utf-8")).hexdigest()

def has_neighbor_pdf(path: Path) -> Path | None:
    if path.suffix.lower() != KEYNOTE_EXT:
        return None
    pdf = path.with_suffix(".pdf")
    return pdf if pdf.exists() else None

def should_skip_path(p: Path) -> bool:
    n = p.name
    if n.startswith("._") or n == ".DS_Store":
        return True
    # Skip anything inside a Keynote package folder (*.key/...) but allow the .key file itself
    if any(part.lower().endswith(".key") for part in p.parts):
        return p.suffix.lower() != ".key"
    return False

def upsert_file(cur, file_id, path, ext, size, modified, project_id, status, rev=None, content_sig=None, text_sig=None):
    cur.execute(
        """
        INSERT OR REPLACE INTO files
        (file_id, path, ext, size, modified, rev, project_id, status, last_indexed, content_sig, text_sig)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """,
        (file_id, path, ext, size, modified, rev, project_id, status, now_utc(), content_sig, text_sig)
    )

def extract_pdf_text(pdf_path: str) -> str:
    try:
        r = PdfReader(pdf_path)
        pages = r.pages[:MAX_PDF_PAGES]
    except Exception:
        return ""

    try:
        text = "\n".join([(p.extract_text() or "") for p in pages])
    except Exception:
        return ""

    return text[:MAX_TEXT_CHARS]

def is_proposal_doc(local_path: str) -> bool:
    return bool(PROPOSAL_DIR_MATCH.search(local_path.replace("\\", " / ")))

def make_project_card(client: OpenAI, text: str) -> str:
    messages = [
        {"role": "system", "content": "You extract project information. Output ONLY valid JSON."},
        {"role": "user", "content":
            "Return JSON with keys: project_name, company, industry, services (array of strings), summary (short paragraph). "
            "If this is not a project/proposal/case-study document, return exactly: {\"not_project\": true}.\n\n"
            f"Document:\n{text}"
        }
    ]
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0,
        response_format={"type": "json_object"},
    )
    return resp.choices[0].message.content

def parse_services(val):
    if isinstance(val, list):
        return [str(x).strip() for x in val if str(x).strip()]
    if isinstance(val, str):
        return [x.strip() for x in val.split(",") if x.strip()]
    return []

def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY missing in .env")

    client = OpenAI(api_key=api_key)
    # Use local Qdrant storage instead of Docker
    qdrant = QdrantClient(path=QDRANT_PATH)
    
    # Create Qdrant collection if it doesn't exist
    from qdrant_client.http.models import VectorParams
    try:
        # Check if collection exists
        qdrant.get_collection(PROJECT_COLLECTION)
        print(f"Qdrant collection '{PROJECT_COLLECTION}' already exists")
    except Exception:
        # Create collection
        qdrant.create_collection(
            collection_name=PROJECT_COLLECTION,
            vectors_config=VectorParams(size=1536, distance="Cosine")
        )
        print(f"Created Qdrant collection '{PROJECT_COLLECTION}'")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    
    # Create tables if they don't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS files (
            file_id TEXT PRIMARY KEY,
            path TEXT,
            ext TEXT,
            size INTEGER,
            modified TEXT,
            rev TEXT,
            project_id TEXT,
            status TEXT,
            last_indexed TEXT,
            content_sig TEXT,
            text_sig TEXT
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            project_id TEXT PRIMARY KEY,
            project_name TEXT,
            company TEXT,
            industry TEXT,
            services TEXT,
            summary TEXT,
            last_indexed TEXT
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS project_sources (
            project_id TEXT,
            file_id TEXT,
            path TEXT,
            PRIMARY KEY (project_id, file_id)
        )
    ''')
    
    con.commit()

    scanned = 0
    meta_only = 0
    pdf_indexed = 0
    project_cards = 0
    errors = 0
    skipped_unchanged = 0

    for root in ROOTS:
        print(f"== Root start: {root} ==")  
        
        for p in Path(root).rglob("*"):
            
            if not p.is_file():
                continue
            if should_skip_path(p):
                continue
            
            scanned += 1
            if scanned % 500 == 0:
                print(f"[{root}] scanned={scanned} pdf_indexed={pdf_indexed} meta_only={meta_only} errors={errors}")
            ext = p.suffix.lower()
            local_path = str(p)

            try:
                st = p.stat()
                size = st.st_size
                mtime_ns = getattr(st, "st_mtime_ns", int(st.st_mtime * 1_000_000_000))
                modified = datetime.datetime.fromtimestamp(st.st_mtime, tz=datetime.timezone.utc).isoformat()
            except Exception:
                size = None
                mtime_ns = None
                modified = None

            fid = file_id_for_path(local_path)
            new_sig = calc_content_sig(size, mtime_ns)
            row_sig = cur.execute("SELECT content_sig FROM files WHERE file_id=?", (fid,)).fetchone()
            old_sig = row_sig[0] if row_sig else None
            row_exists = cur.execute("SELECT 1 FROM files WHERE file_id=?", (fid,)).fetchone()
            if row_exists and old_sig and new_sig and old_sig == new_sig:
                if ext == ".pdf" and is_online_only(local_path):
                    upsert_file(cur, fid, local_path, ext, size, modified, None, "online_only", content_sig=new_sig)
                    meta_only += 1
                    continue

                skipped_unchanged += 1
                cur.execute("UPDATE files SET last_indexed=? WHERE file_id=?", (now_utc(), fid))
                continue
            

            try:
                # Keynote: metadata-only unless there is a neighboring PDF
                if ext == KEYNOTE_EXT:
                    if has_neighbor_pdf(p):
                        upsert_file(cur, fid, local_path, ext, size, modified, None, "shadowed_by_pdf", content_sig=new_sig)
                    else:
                        upsert_file(cur, fid, local_path, ext, size, modified, None, "metadata_only", content_sig=new_sig)
                        meta_only += 1
                    continue

                # Always store metadata
                if not row_exists:
                    upsert_file(cur, fid, local_path, ext, size, modified, None, "seen", content_sig=new_sig)

                # PDF content indexing
                if ext in CONTENT_EXTS:
                    
                  #  if ext == ".pdf" and is_online_only(local_path):
                   #     upsert_file(cur, fid, local_path, ext, size, modified, None, "online_only", content_sig=new_sig)
                  #      meta_only += 1
                    #    continue
                    
                    if size and size > MAX_PDF_BYTES:
                        upsert_file(cur, fid, local_path, ext, size, modified, None, "metadata_only_too_large", content_sig=new_sig)
                        meta_only += 1
                        continue

                   #if old_sig and new_sig and old_sig == new_sig:
                    #    status = "skipped_unchanged"
                     #   upsert_file(cur, fid, local_path, ext, size, modified, None, status, content_sig=new_sig)
                      #  continue
                    
                    
                    
                    text = extract_pdf_text(local_path)
                    if not text.strip():
                        upsert_file(cur, fid, local_path, ext, size, modified, None, "metadata_only_no_text", content_sig=new_sig)
                        meta_only += 1
                        continue

                    pdf_indexed += 1

                    # Only create project cards in proposal-ish areas
                    if is_proposal_doc(local_path):
                        raw_json = make_project_card(client, text)

                        import json
                        try:
                            data = json.loads(raw_json)
                        except Exception:
                            errors += 1
                            upsert_file(cur, fid, local_path, ext, size, modified, None, "project_parse_invalid_json", content_sig=new_sig)
                            continue

                        if data.get("not_project") is True:
                            upsert_file(cur, fid, local_path, ext, size, modified, None, "indexed_no_project", content_sig=new_sig)
                            continue

                        project_name = (data.get("project_name") or "").strip()
                        company = (data.get("company") or "").strip()
                        industry = (data.get("industry") or "").strip()
                        services = parse_services(data.get("services"))
                        summary = (data.get("summary") or "").strip()

                        if not project_name or not company or not summary:
                            upsert_file(cur, fid, local_path, ext, size, modified, None, "project_parse_missing_fields", content_sig=new_sig)
                            continue

                        project_id = hashlib.md5((project_name + "|" + company).encode("utf-8")).hexdigest()

                        # DB
                        cur.execute(
                            "INSERT OR REPLACE INTO projects VALUES (?,?,?,?,?,?,?)",
                            (project_id, project_name, company, industry, ", ".join(services), summary, now_utc())
                        )
                        cur.execute(
                            "INSERT OR REPLACE INTO project_sources VALUES (?,?,?)",
                            (project_id, fid, local_path)
                        )

                        print(f"Creating project card for {project_name} ({company})")
                        # Vector
                        embed_input = f"{project_name} | {company} | {industry} | {', '.join(services)} | {summary}"
                        emb = client.embeddings.create(model="text-embedding-3-small", input=embed_input).data[0].embedding
                        point = PointStruct(
                            id=int(project_id[:8], 16),
                            vector=emb,
                            payload={
                                "project_id": project_id,
                                "project_name": project_name,
                                "company": company,
                                "industry": industry,
                                "services": services,
                                "summary": summary,
                                "path": local_path,
                            }
                        )
                        qdrant.upsert(collection_name=PROJECT_COLLECTION, points=[point])
                        print(f"Upserted to Qdrant collection '{PROJECT_COLLECTION}'")

                        upsert_file(cur, fid, local_path, ext, size, modified, project_id, "project_card_created", content_sig=new_sig)
                        project_cards += 1

            except Exception as e:
                errors += 1
                upsert_file(cur, fid, local_path, ext, size, modified, None, f"error:{type(e).__name__}")

            if scanned % 50 == 0:
                con.commit()
        print(f"== Root done: {root} | scanned={scanned} pdf_indexed={pdf_indexed} meta_only={meta_only} errors={errors} ==")

    con.commit()
    con.close()
    qdrant.close()

    print("DONE")
    print("scanned:", scanned)
    print("meta_only:", meta_only)
    print("pdf_with_text:", pdf_indexed)
    print("project_cards_created:", project_cards)
    print("errors:", errors)
    print("skipped_unchanged:", skipped_unchanged)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n== CANCELLED BY USER (Ctrl-C) ==")