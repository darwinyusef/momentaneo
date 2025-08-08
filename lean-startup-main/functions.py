# ~ functions.py | core api's functions
import sqlite3

def parse_sqlite(tuples: tuple):
    if len(tuples) <= 0:
        return
    structured_data = []
    for tup in tuples:
        structured_data.append({
            "id": tup[0],
            "name": tup[1],
            "definition": tup[2],
            "book_section": tup[3]
        })
    if len(tuples) > 1:
        return structured_data
    else:
        return structured_data[0]

def create_concepts_database(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS concepts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        definition TEXT NOT NULL,
        book_section TEXT NOT NULL
    )
    ''')