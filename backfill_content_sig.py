import sqlite3, hashlib

DB = r"C:\Users\Bastian\rag_db\rag_state.sqlite"
ROOT1 = r"\Propelland Dropbox\01 Client Projects"
ROOT2 = r"\Propelland Dropbox\02 Business Development"

def sig(size, modified):
    if size is None or modified is None:
        return None
    return hashlib.md5(f"{size}|{modified}".encode("utf-8")).hexdigest()

con = sqlite3.connect(DB)
cur = con.cursor()

rows = cur.execute("""
    SELECT file_id, size, modified
    FROM files
    WHERE content_sig IS NULL
      AND (instr(path, ?) > 0 OR instr(path, ?) > 0)
""", (ROOT1, ROOT2)).fetchall()

updated = 0
for file_id, size, modified in rows:
    s = sig(size, modified)
    if not s:
        continue
    cur.execute("UPDATE files SET content_sig=? WHERE file_id=?", (s, file_id))
    updated += 1

con.commit()
con.close()
print(f"Backfilled content_sig for {updated} rows")