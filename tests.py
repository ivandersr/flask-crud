import pytest
import requests

BASE_URL = 'http://localhost:5000'
tasks = []

def test_create_task():
    new_task_data = {
        "title": "Nova tarefa",
        "description": "Descrição da nova tarefa",
    }

    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    assert response.status_code == 200
    response_json = response.json()
    assert "description" in response_json
    assert "title" in response_json
    assert "id" in response_json
    tasks.append(response_json["id"])

def test_get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200
    response_json = response.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json
    assert len(response_json["tasks"]) == len(tasks)

def test_find_task():
    if tasks:
        response = requests.get(f"{BASE_URL}/tasks/{tasks[0]}")
        assert response.status_code == 200
        response_json = response.json()
        assert "description" in response_json
        assert "title" in response_json
        assert "completed" in response_json
        assert "id" in response_json

def test_find_task_not_found():
    response = requests.get(f"{BASE_URL}/tasks/99999")
    assert response.status_code == 404
    assert response.json()["message"] == "Task not found"

def test_update_task():
    payload = {
        "description":"Teste update task",
        "completed": True,
        "title": "Teste update task"
    }
    if tasks:
        response = requests.put(f"{BASE_URL}/tasks/{tasks[0]}", json=payload)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["description"] == payload["description"]
        assert response_json["completed"] == payload["completed"]
        assert response_json["title"] == payload["title"]

def test_delete_task():
    if tasks:
        response = requests.delete(f"{BASE_URL}/tasks/{tasks[0]}")
        assert response.status_code == 200
        response_json = response.json()
        assert "id" in response_json
        response = requests.get(f"{BASE_URL}/tasks/{tasks[0]}")
        assert response.status_code == 404
   