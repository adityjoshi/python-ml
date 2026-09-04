from typing import Literal, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
import uvicorn

import models
from database import Base, engine, get_db
from schemas import (
    NotebookCreate,
    NotebookOut,
    NotebookWithEntries,
    EntryCreate,
    EntryOut,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/notebooks", response_model=NotebookOut, status_code=201)
def create_notebook(
    notebook: NotebookCreate, db: Session = Depends(get_db)
) -> NotebookOut:
    new_book = models.Notebook(
        title=notebook.title,
        author=notebook.author,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.post("/notebooks/{notebook_id}/entries", response_model=EntryOut, status_code=201)
def add_entry(
    notebook_id: int, entry: EntryCreate, db: Session = Depends(get_db)
) -> EntryOut:
    notebook = (
        db.query(models.Notebook)
        .filter(models.Notebook.id == notebook_id)
        .first()
    )
    if notebook is None:
        raise HTTPException(
            status_code=404,
            detail=f"No notebook found with id {notebook_id}",
        )

    db_entry = models.Entry(
        heading=entry.heading,
        mood=entry.mood,
        word_count=entry.word_count,
        notebook_id=notebook_id,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@app.get("/notebooks/{notebook_id}", response_model=NotebookWithEntries, status_code=200)
def get_notebook(
    notebook_id: int,
    mood: Optional[str] = None,
    sort: Optional[Literal["heading", "word_count"]] = Query(None),
    db: Session = Depends(get_db),
) -> NotebookWithEntries:
    notebook = (
        db.query(models.Notebook)
        .filter(models.Notebook.id == notebook_id)
        .first()
    )
    if notebook is None:
        raise HTTPException(
            status_code=404,
            detail=f"No notebook found with id {notebook_id}",
        )

    entry_q = db.query(models.Entry).filter(models.Entry.notebook_id == notebook_id)

    if mood is not None:
        entry_q = entry_q.filter(models.Entry.mood == mood)
    if sort == "heading":
        entry_q = entry_q.order_by(models.Entry.heading.asc())
    elif sort == "word_count":
        entry_q = entry_q.order_by(models.Entry.word_count.asc())

    entries = entry_q.all()

    return NotebookWithEntries(
        id=notebook.id,
        title=notebook.title,
        author=notebook.author,
        entries=entries,
    )


@app.delete("/notebooks/{notebook_id}/entries", status_code=204)
def clear_entries(
    notebook_id: int, db: Session = Depends(get_db)
) -> None:
    notebook = (
        db.query(models.Notebook)
        .filter(models.Notebook.id == notebook_id)
        .first()
    )
    if notebook is None:
        raise HTTPException(
            status_code=404,
            detail=f"No notebook found with id {notebook_id}",
        )

    db.query(models.Entry).filter(models.Entry.notebook_id == notebook_id).delete()
    db.commit()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
