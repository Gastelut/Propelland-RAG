import sqlite3

DB = r"C:\Users\Bastian\rag_db\rag_state.sqlite"
PATTERN = r"\Esteban Gastelut"

def table_columns(cur, table):
    return [r[1] for r in cur.execute(f"PRAGMA table_info({table})").fetchall()]

con = sqlite3.connect(DB)
cur = con.cursor()

# tables that typically exist in this project
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

con.execute("BEGIN")

deleted_total = 0

for t in tables:
    cols = table_columns(cur, t)
    path_cols = [c for c in cols if "path" in c.lower()]  # path, source_path, file_path, etc.
    for c in path_cols:
        # delete rows where that column contains the Esteban folder
        cur.execute(f"DELETE FROM {t} WHERE instr({c}, ?) > 0", (PATTERN,))
        deleted_total += cur.rowcount

# remove orphan projects (projects with no remaining sources)
if "projects" in tables and "project_sources" in tables:
    proj_cols = table_columns(cur, "projects")
    src_cols = table_columns(cur, "project_sources")
    if "project_id" in proj_cols and "project_id" in src_cols:
        cur.execute("""
            DELETE FROM projects
            WHERE project_id NOT IN (SELECT DISTINCT project_id FROM project_sources)
        """)
        deleted_total += cur.rowcount

con.commit()
con.close()

print(f"OK - deleted {deleted_total} rows related to: {PATTERN}")