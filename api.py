from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import creat_tables, get_connection

app = FastAPI()
creat_tables()


class TaskCreate(BaseModel):
    title: str
    priority: str


@app.get("/")
def root():
    return {"message": "任务管理API运行成功"}


@app.get("/tasks")
def get_tasks():
    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT id,title,priority,completed
        FROM tasks
        ORDER BY id
        """
    )
    rows = cursor.fetchall()
    task_list = []

    for row in rows:
        task = dict(row)
        task["completed"] = bool(task["completed"])
        task_list.append(task)

    connection.close()

    return {
        "count": len(task_list),
        "data": task_list,

    }


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT id,title,priority,completed
        FROM tasks
        WHERE id =?
        """,
        (task_id,),
    )
    row = cursor.fetchone()
    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="没找到这个任务",
        )
    task = dict(row)
    task["completed"] = bool(task["completed"])

    return task


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    title = task.title.strip()
    priority = task.priority.strip()

    if title == "":
        raise HTTPException(
            status_code=400,
            detail="任务标题不能为空",
        )

    if priority not in ["高", "中", "低"]:
        raise HTTPException(
            status_code=400,
            detail="优先级只能是高，中，低",
        )

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO tasks(title,priority,completed)
        VALUES(?,?,?)
        """,
        (title, priority, 0),

    )
    connection.commit()

    task_id = cursor.lastrowid
    connection.close()

    return {
        "id": task_id,
        "title": title,
        "priority": priority,
        "completed": False,
    }


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate):
    title = task.title.strip()
    priority = task.priority.strip()

    if title == "":
        raise HTTPException(
            status_code=400,
            detail="任务标题不能为空"

        )
    if priority not in ["高", "中", "低"]:
        raise HTTPException(
            status_code=400,
            detail="优先级只能是高，中，低"

        )


    connection = get_connection()
    cursor = connection.execute(
        """
        UPDATE tasks
        SET title=?,priority=?
        WHERE id =?
        """,
        (title, priority, task_id),
    )
    connection.commit()

    if cursor.rowcount == 0:
        connection.close()

        raise HTTPException(
        status_code=404,
        detail="没有找到这个任务",
        )
    cursor = connection.execute(
        """
        SELECT id,title,priority,completed
        FROM tasks
        WHERE id = ?
        """,
        (task_id,),
    )
    row = cursor.fetchone()
    connection.close()
    updated_task = dict(row)
    updated_task["completed"] = bool(updated_task["completed"])

    return updated_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    connection = get_connection()
    cursor = connection.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (task_id,),
    )

    connection.commit()
    deleted_count=cursor.rowcount
    connection.close()

    if deleted_count ==0:
        raise  HTTPException(
            status_code=404,
            detail="没有找到这个任务",
        )
    return {
        "message":"任务删除成功",
        "id":task_id,
    }


