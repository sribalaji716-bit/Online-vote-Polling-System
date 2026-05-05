import sqlite3
from pathlib import Path
path = Path('db.sqlite3')
conn = sqlite3.connect(path)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'voting_%';")
print('voting tables', cur.fetchall())
for table in ['voting_voter', 'voting_position', 'voting_candidate', 'voting_votes']:
    try:
        cur.execute(f"PRAGMA table_info({table});")
        print(table, cur.fetchall())
    except Exception as e:
        print('error', table, e)
conn.close()
