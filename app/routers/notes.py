from fastapi import APIRouter, HTTPException, Depends
from app.db import get_db_connection
from app.schemas import NoteIn, NoteOut
import sqlite3

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=NoteOut, status_code=201)    
def create_note(note: NoteIn, db: sqlite3.Connection = Depends(get_db_connection)):
	cursor = db.cursor()
	cursor.execute(
		"INSERT INTO notes (title, content, completed) VALUES (?, ?, ?)", 
		(note.title, note.content, note.completed)
	)
	db.commit()
      
  # Retrieve the newly inserted item record
	note_id = cursor.lastrowid
	cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
	row = cursor.fetchone()
	return dict(row)
    
