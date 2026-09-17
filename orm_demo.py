from sqlalchemy import Boolean, String, create_engine,select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    priority: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )
    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )


engine = create_engine(
    "sqlite:///tasks_orm.db",
    echo=True,
)
Base.metadata.create_all(engine)

task_id_text = input("请输入要修改的任务ID：").strip()

try:
    task_id = int(task_id_text)
except ValueError:
    print("任务id必须是整数")
    raise  SystemExit

with Session(engine) as session:
    task = session.get(Task,task_id)

    if task is None:
        print("没有找到这个任务")
    else:
        new_title = input("请输入新标题：").strip()

        while new_title == "":
            print("标题不能为空")
            new_title = input("请输入新标题").strip()

        new_priority = input("请输入新优先级高，中，低：").strip()

        while new_priority not in ["高","中","低"]:
            print("优先级只能是高，中，低")
            new_priority = input("请重新输入优先级高，中，低").strip()

        task.title = new_title
        task.priority = new_priority

        session.commit()
        session.refresh(task)
        print("任务修改成功")
        print("ID：", task.id)
        print("标题：", task.title)
        print("优先级：", task.priority)
        print("完成状态：", task.completed)

