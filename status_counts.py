import sqlite3

DB = r"C:\Users\Bastian\rag_db\rag_state.sqlite"

ROOT1 = r"\Propelland Dropbox\01 Client Projects"
ROOT2 = r"\Propelland Dropbox\02 Business Development"

con = sqlite3.connect(DB)
cur = con.cursor()

q = """
select status, count(1)
from files
where instr(path, ?) > 0
   or instr(path, ?) > 0
group by status
order by count(1) desc
"""
print(cur.execute(q, (ROOT1, ROOT2)).fetchall())

con.close()