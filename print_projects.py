import sqlite3
DB_PATH = r"C:\Users\Bastian\propelland-rag-data\db\rag_state.sqlite"

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

print("=== All Projects ===")
cur.execute('SELECT project_name, company, summary FROM projects')
for row in cur.fetchall():
    print(f'{row[0]} ({row[1]})')
    print(f'  {row[2]}')
    print()

con.close()