# ~ main.py | core api

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3, uvicorn, dotenv, os
import functions

dotenv.load_dotenv()

app = FastAPI()

# consts
DATABASE_PATH = "book.sqlite3"
if not os.path.exists(DATABASE_PATH):
    functions.create_concepts_database(DATABASE_PATH)

class Concept(BaseModel):
    name:           str
    definition:     str
    book_section:   str

@app.post("/concepts")
def create_concept(concept: Concept):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO concepts (name, definition, book_section) VALUES (?, ?, ?)",
        (concept.name, concept.definition, concept.book_section)
    )    
    conn.commit()
    if cursor.fetchone():
        raise HTTPException(status_code=200, detail="Concept created successfully.")
        conn.close()
    else:
        raise HTTPException(status_code=500, detail="Something went wrong.")
        conn.close()

@app.get("/concepts")
def get_concepts():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM concepts")
    rows = cursor.fetchall()

    return functions.parse_sqlite(rows)

@app.get("/concepts/{unique_id}")
def get_concept(unique_id: int):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM concepts WHERE id = ?", (str(unique_id)))
    
    row = cursor.fetchall()
    if row:
        return functions.parse_sqlite(row)
        conn.close()
    else:
        raise HTTPException(status_code=404, detail="Concept not found.")
        conn.close()

@app.put("/concepts/{unique_id}")
def update_concept(unique_id: int, concept: Concept):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE concepts SET name = ?, definition = ?, book_section = ? WHERE id = ?", (concept.name,concept.definition,concept.book_section,str(unique_id)))
    result = cursor.fetchone()
    conn.commit()
    if result:
        HTTPException(status_code=200),
    else:
        HTTPException(status_code=404)

@app.delete("/concepts/{unique_id}")
def delete_concept(unique_id: int):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM concepts WHERE id = ?", (str(unique_id)))
    result = cursor.fetchone()
    conn.commit()
    if result:
        HTTPException(status_code=200),
    else:
        HTTPException(status_code=404)


uvicorn.run(app, port=int(os.getenv("DEPLOY_PORT")), host=os.getenv("DEPLOY_HOST"))