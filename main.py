import json


def save_tasks(tasks):
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)

        print("任务已保存")


def load_tasks():
    try:
        with open("tasks.json", "r", encoding="utf-8") as file:
            tasks = json.load(file)
        print("历史任务加载成功")
        return tasks

    except FileNotFoundError:
        print("没有找到历史任务，将创建新的任务列表")
        return []

    except json.JSONDecodeError:
        print("任务文件格式错误，将使用空任务列表")
        return []


def show_tasks(tasks):
    if len(tasks) == 0:
        print("暂无任务")
        return
    for item in tasks:
        if item["completed"]:
            status = "已完成"
        else:
            status = "未完成"
        priority = item.get("priority", "中")
        print(f"[{status}] ID: {item['id']} |"
              f"优先级：{priority} | {item['title']}")


def search_tasks(tasks):
    keyword = input("请输入关键词：").strip()

    if keyword == "":
        print("不能输入为空")
        return

    found = False

    for item in tasks:
        if keyword.lower() in item["title"].lower():
            if item["completed"]:
                status = "已完成"
            else:
                status = "未完成"
            print(f"[{status}] ID:{item['id']} | {item['title']}")
            found = True

    if not found:
        print("没有找到相关任务")


def get_next_id(tasks):
    max_id = 0

    for item in tasks:
        if item["id"] > max_id:
            max_id = item["id"]
    return max_id + 1


def add_task(tasks):
    new_title = input("请输入标题：").strip()
    while new_title == "":
        print("不能为空")
        new_title = input("请输入标题：").strip()
    priority = input("请输入优先级（高，中，低）：").strip()
    while priority not in ["高", "中", "低"]:
        print("优先级只能是高，中，低")
        priority = input("请输入优先级（高，中，低）：").strip()
    new_task = {
        "id": get_next_id(tasks),
        "title": new_title,
        "priority": priority,
        "completed": False,
    }
    tasks.append(new_task)
    print("任务添加成功")


def complete_task(tasks):
    if len(tasks) == 0:
        print("暂无任务")
        return
    task_id_text = input("请输入要完成任务的id：").strip()

    try:
        task_id = int(task_id_text)
    except ValueError:
        print("必须是整数")
        return
    for item in tasks:
        if item["id"] == task_id:
            item["completed"] = True
            print("任务已完成")
            return
    print("没有找到这个任务")


def delete_task(tasks):
    if len(tasks) == 0:
        print("暂无任务")
        return
    delete_id_text = input("请输入要删除任务的id：").strip()

    try:
        delete_id = int(delete_id_text)
    except ValueError:
        print("任务id必须是整数")
        return

    for item in tasks:
        if item["id"] == delete_id:
            tasks.remove(item)
            print("任务已删除")
            return

    print("未找到该任务")


def update_task(tasks):
    if len(tasks) == 0:
        print("暂无任务")
        return

    task_id_text = input("请输入要修改的id:").strip()

    try:
        task_id = int(task_id_text)
    except ValueError:
        print("这个数必须是整数")
        return

    for item in tasks:
        if item["id"] == task_id:
            new_title = input("请输入新标题：").strip()

            while new_title == "":
                print("标题不能为空")
                new_title = input("请输入新标题：").strip()

            new_priority = input("请重新输入新的优先级：").strip()

            while new_priority not in ["高", "中", "低"]:
                print("优先级只能是高，中，低")
                new_priority = input("请重新输入新的优先级：").strip()

            item["title"] = new_title
            item["priority"] = new_priority
            print("修改完成")
            return

    print("没有找到这个id")


def show_menu():
    print()
    print("====任务管理器====")
    print("1 添加任务")
    print("2 查看任务")
    print("3 完成任务")
    print("4 删除任务")
    print("5 搜索任务")
    print("6 修改任务")
    print("7 退出")


tasks = load_tasks()
while True:
    show_menu()
    choice = input("请选择操作：").strip()

    if choice == "1":
        add_task(tasks)
        save_tasks(tasks)
    elif choice == "2":
        show_tasks(tasks)
    elif choice == "3":
        complete_task(tasks)
        save_tasks(tasks)
    elif choice == "4":
        delete_task(tasks)
        save_tasks(tasks)
    elif choice == "5":
        search_tasks(tasks)
    elif choice == "6":
        update_task(tasks)
        save_tasks(tasks)
    elif choice == "7":
        print("程序退出")
        break
    else:
        print("输入无效，请输入正确格式")
