import sqlite3
from pathlib import Path
path = Path('db.sqlite3')
print('DB exists', path.exists())
conn = sqlite3.connect(path)
cur = conn.cursor()
cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name='voting_voter';")
print(cur.fetchone())
cur.execute("PRAGMA table_info(voting_voter);")
print(cur.fetchall())
cur.execute("SELECT app, name FROM django_migrations ORDER BY app, name LIMIT 20;")
rows = cur.fetchall()
print(rows)
conn.close()
