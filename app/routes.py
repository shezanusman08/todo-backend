from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import engine
from app.models import Todo

router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


@router.get("/todos")
def get_todos(session: Session = Depends(get_session)):
    return session.exec(select(Todo)).all()


@router.post("/todos")
def create_todo(title: str, session: Session = Depends(get_session)):
    todo = Todo(title=title)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@router.put("/todos/{todo_id}/complete")
def complete_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Not found")

    todo.completed = True
    session.add(todo)
    session.commit()
    return {"message": "completed"}


@router.put("/todos/{todo_id}")
def toggle_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.completed = not todo.completed
    session.add(todo)
    session.commit()
    return todo


@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    session.delete(todo)
    session.commit()
    return {"ok": True}
