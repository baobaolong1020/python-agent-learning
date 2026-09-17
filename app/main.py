from fastapi import Depends, FastAPI, HTTPException
from app import models, schemas
from app.database import Base, engine, get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="任务管理API",
)


@app.get("/")
def root():
    return {
        "message": "SQLAlchemy版任务API运行成功"
    }


@app.post(
    "/tasks",
    response_model=schemas.TaskResponse,
    status_code=201,
)
def create_task(
    task_data: schemas.TaskCreate,
    session: Session = Depends(get_db),
):
    title = task_data.title.strip()

    if title == "":
        raise HTTPException(
            status_code=400,
            detail="任务标题不能为空",
        )

    new_task = models.Task(
        title=title,
        priority=task_data.priority,
        completed=False,
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task


@app.get(
    "/tasks",
    response_model=list[schemas.TaskResponse],
)
def get_tasks(
    session: Session = Depends(get_db),
):
    statement = select(models.Task).order_by(
        models.Task.id
    )

    task_list = session.scalars(statement).all()

    return task_list

@app.get(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse,
)
def get_task(
    task_id: int,
    session: Session = Depends(get_db),
):
    task = session.get(
        models.Task,
        task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="没有找到这个任务",
        )

    return task


@app.put(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse,
)
def update_task(
    task_id: int,
    task_data: schemas.TaskCreate,
    session: Session = Depends(get_db),
):
    title = task_data.title.strip()

    if title == "":
        raise HTTPException(
            status_code=400,
            detail="任务标题不能为空",
        )

    task = session.get(
        models.Task,
        task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="没有找到这个任务",
        )

    task.title = title
    task.priority = task_data.priority

    session.commit()
    session.refresh(task)

    return task

@app.delete(
    "/tasks/{task_id}",
    response_model=schemas.TaskDeleteResponse,
)
def delete_task(
    task_id: int,
    session: Session = Depends(get_db),
):
    task = session.get(
        models.Task,
        task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="没有找到这个任务",
        )

    deleted_id = task.id

    session.delete(task)
    session.commit()

    return {
        "message": "任务删除成功",
        "id": deleted_id,
    }