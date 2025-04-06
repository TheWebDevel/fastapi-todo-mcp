from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Session, Mapped, mapped_column

from database import Base


class ToDo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(String)
    session_key: Mapped[str] = mapped_column(String)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)  # New column added


def create_todo(db: Session, content: str, session_key: str, notes: str = None):
    todo = ToDo(content=content, session_key=session_key, notes=notes)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_todo(db: Session, item_id: int):
    return db.query(ToDo).filter(ToDo.id == item_id).first()


def update_todo(db: Session, item_id: int, content: str, notes: str = None):
    todo = get_todo(db, item_id)
    todo.content = content
    if notes is not None:
        todo.notes = notes
    db.commit()
    db.refresh(todo)
    return todo


def get_todos(db: Session, session_key: str, skip: int = 0, limit: int = 100):
    return db.query(ToDo).filter(ToDo.session_key == session_key).offset(skip).limit(limit).all()


def delete_todo(db: Session, item_id: int):
    todo = get_todo(db, item_id)
    db.delete(todo)
    db.commit()