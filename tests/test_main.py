from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "SQLAlchemy版任务API运行成功"
    }


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "测试创建任务",
            "priority": "高",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "测试创建任务"
    assert data["priority"] == "高"
    assert data["completed"] is False

    get_response = client.get("/tasks")

    assert get_response.status_code == 200
    assert len(get_response.json()) == 1


def test_get_missing_task(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "没有找到这个任务"
    }


def test_create_task_with_invalid_priority(client):
    response = client.post(
        "/tasks",
        json={
            "title": "测试错误优先级",
            "priority": "紧急",
        },
    )

    assert response.status_code == 422


def test_create_task_with_blank_title(client):
    response = client.post(
        "/tasks",
        json={
            "title": "   ",
            "priority": "高",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "任务标题不能为空"
    }


def test_create_task_with_default_priority(client):
    response = client.post(
        "/tasks",
        json={
            "title": "测试默认优先级"
        },
    )

    assert response.status_code == 201
    assert response.json()["priority"] == "中"


def test_update_and_delete_task(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "原始任务",
            "priority": "高",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    update_response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "修改后的任务",
            "priority": "低",
        },
    )

    assert update_response.status_code == 200
    assert update_response.json()["title"] == "修改后的任务"
    assert update_response.json()["priority"] == "低"

    get_response = client.get(
        f"/tasks/{task_id}"
    )

    assert get_response.status_code == 200
    assert get_response.json()["title"] == "修改后的任务"

    delete_response = client.delete(
        f"/tasks/{task_id}"
    )

    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "任务删除成功",
        "id": task_id,
    }

    missing_response = client.get(
        f"/tasks/{task_id}"
    )

    assert missing_response.status_code == 404


def test_update_missing_task(client):
    response = client.put(
        "/tasks/999",
        json={
            "title": "不存在的任务",
            "priority": "高",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "没有找到这个任务"
    }


def test_delete_missing_task(client):
    response = client.delete("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "没有找到这个任务"
    }

def test_database_is_empty_at_start(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []