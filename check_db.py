import sqlite3
from pathlib import Path

DB_PATH = r"C:\Users\Bastian\propelland-rag-data\db\rag_state.sqlite"

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

print("=== Files Table ===")
cur.execute('SELECT COUNT(*) FROM files')
print(f"Total files: {cur.fetchone()[0]}")

cur.execute('SELECT ext, COUNT(*) FROM files GROUP BY ext')
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]} files")

cur.execute('SELECT status, COUNT(*) FROM files GROUP BY status')
print("\n=== Status Distribution ===")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]} files")

cur.execute('SELECT COUNT(*) FROM projects')
print(f"\n=== Projects Table ===")
print(f"Total projects: {cur.fetchone()[0]}")

# Print all projects
cur.execute('SELECT project_id, project_name, company FROM projects')
for row in cur.fetchall():
    print(f"  {row[1]} ({row[2]})")

# Print first 10 file paths to see what we're indexing
print("\n=== First 10 File Paths ===")
cur.execute('SELECT path FROM files LIMIT 10')
for row in cur.fetchall():
    print(f"  {row[0]}")

con.close()