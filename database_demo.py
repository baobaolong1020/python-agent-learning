import sqlite3

connection = sqlite3.connect("tasks.db")
cursor = connection.cursor()

cursor.execute(
    """
     CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        priority TEXT NOT NULL,
        completed INTEGER NOT NULL
     )
    """

)

#cursor.execute(
#    """
#    INSERT INTO tasks (title,priority,completed)
#    VALUES(?,?,?)
#    """,
#    ("学习sqlite","高",0),
#)
#connection.commit()

task_id_text = input("请输入要删除的任务id：").strip()

try:
    task_id = int(task_id_text)
except ValueError:
    print("任务id必须是整数")
    connection.close()
    raise SystemExit

cursor.execute(
    """
    
    DELETE FROM tasks
    WHERE id = ?
    """,
    (task_id,),
)

connection.commit()

if cursor.rowcount == 0:
    print("没有找到这个任务")
else:
    print("任务删除成功")

    cursor.execute(
        """
        SELECT id,title,priority,completed
        FROM tasks
        """
    )
    rows = cursor.fetchall()
    if len(rows)==0:
        print("数据库中暂无任务")
    else:
        print("当前剩余任务：")

        for row in rows:
            print(row)

connection.close()