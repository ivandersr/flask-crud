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