import os
import sqlite3, sys

db = r"C:\Users\Bastian\propelland-rag-data\db\rag_state.sqlite"
query = " ".join(sys.argv[1:]).strip()
if not query:
    raise SystemExit('Usage: py find_files.py "cimd proposal"')

terms = [t.lower() for t in query.split() if t.strip()]

con = sqlite3.connect(db)
cur = con.cursor()

rows = cur.execute(
    "SELECT f.path, f.ext, f.status, p.project_name, p.company, p.industry, p.services "
    "FROM files f LEFT JOIN projects p ON f.project_id = p.project_id"
).fetchall()

hits = []
for row in rows:
    path, ext, status, pname, company, industry, services = row
    if not path:
        continue

    # hide macOS sidecar junk + keynote package internals
    if "\\._" in path or "/._" in path:
        continue
    if ".key\\" in path.lower() or ".key/" in path.lower():
        continue

    blob = " ".join([
        path,
        str(pname or ""),
        str(company or ""),
        str(industry or ""),
        str(services or "")
    ]).lower()

    if all(t in blob for t in terms):
        hits.append(row)

for i, row in enumerate(hits[:30], start=1):
    path, ext, status, pname, company, industry, services = row
    safe_path = (path or "").replace("\n", " ").replace("\r", " ")
    print(f"{i:02d}. {safe_path}")
    print(f"    Folder: {os.path.dirname(safe_path)}")
    if pname:
        print(f"    Project: {(pname or '').replace('\n',' ').replace('\r',' ')}")
        print(f"    Company: {(company or '').replace('\n',' ').replace('\r',' ')}")
        print(f"    Industry: {(industry or '').replace('\n',' ').replace('\r',' ')}")
        print(f"    Services: {(services or '').replace('\n',' ').replace('\r',' ')}")
    print()

print(f"Total hits: {len(hits)}")
con.close()