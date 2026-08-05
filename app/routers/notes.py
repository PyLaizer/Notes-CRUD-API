from fastapi import APIRouter, HTTPException, Depends, Query
from app.db import get_db_connection
from app.schemas import NoteIn, NoteOut, NotePatch
from typing import Optional
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
      
	note_id = cursor.lastrowid
	cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
	row = cursor.fetchone()
	return dict(row)
    
@router.get("/", response_model=list[NoteOut], status_code=200)    
def get_notes(completed: Optional[bool] = Query(None), db: sqlite3.Connection = Depends(get_db_connection)):
	"""Fetches all items from the database."""
	cursor = db.cursor()
	if completed is not None:
		cursor.execute("SELECT * FROM notes WHERE completed = ?", (1 if completed else 0,))
	else:
		cursor.execute("SELECT * FROM notes")
	rows = cursor.fetchall()
	return [dict(row) for row in rows]

@router.get("/{note_id}", response_model=NoteOut, status_code=200)    
def get_note(note_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
	"""Fetches  a specific note by its ID."""
	cursor = db.cursor()
	cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
	row = cursor.fetchone()

	if row is None:
		raise HTTPException(status_code=404, detail="Note not found")
	return dict(row)

@router.put("/{note_id}", response_model=NoteOut, status_code=200)    
def update_note(note_id: int, note: NoteIn, db: sqlite3.Connection = Depends(get_db_connection)):
	"""Fully Update a specific note by its ID."""
	cursor = db.cursor()
	cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
	row = cursor.fetchone()

	if row is None:
		raise HTTPException(status_code=404, detail="Note not found")
	cursor.execute("UPDATE notes SET title = ?, content = ?, completed = ? WHERE id = ?",(note.title, note.content, int(note.completed), note_id))
	db.commit()

	cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
	row = cursor.fetchone()
	return dict(row)

@router.patch("/{note_id}", response_model=NoteOut, status_code=200)  
def partial_update_note(note_id: int, note: NotePatch, db: sqlite3.Connection = Depends(get_db_connection)):
	"""Partially Update a specific note by its ID."""
	cursor = db.cursor()
	cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
	row = cursor.fetchone()

	if row is None:
		raise HTTPException(status_code=404, detail="Note not found")
	current_data = dict(row)

	update_data = note.model_dump(exclude_unset=True)
	if not update_data:
		return {"id": note_id, **current_data}
	query_parts = []
	query_values = []
    
	for key, value in update_data.items():
			query_parts.append(f"{key} = ?")
			query_values.append(value)

	query_values.append(note_id)
	sql_query = f"UPDATE notes SET {', '.join(query_parts)} WHERE id = ?"
	cursor.execute(sql_query, tuple(query_values))
	db.commit()

	cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
	row = cursor.fetchone()
	return dict(row)

