from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database, cache

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)


@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = cache.get_task(task_id)
    if not task:
        task = crud.get_task(db, task_id=task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        cache.set_task(task_id, task)
    return task


@app.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = cache.get_tasks(skip, limit)
    if not tasks:
        tasks = crud.get_tasks(db, skip=skip, limit=limit)
        cache.set_tasks(skip, limit, tasks)
    return tasks


@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db=db, task=task, task_id=task_id)


@app.patch("/tasks/{task_id}", response_model=schemas.Task)
def partial_update_task(task_id: int, task: schemas.TaskPatch, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.partial_update_task(db=db, task=task, task_id=task_id)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db=db, task_id=task_id)
    cache.delete_task(task_id)
    return None
