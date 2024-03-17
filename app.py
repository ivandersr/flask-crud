from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_control_id = 1

@app.route("/tasks", methods=["POST"])
def create_new_task():
    global task_control_id
    title, description = request.get_json()
    task = Task(task_control_id, title, description)
    task_control_id += 1
    tasks.append(task)
    return jsonify(task.to_dict())

@app.route("/tasks", methods=["GET"])
def list_tasks():
    task_list = [task.to_dict() for task in tasks]

    return jsonify({
        "tasks": task_list,
        "total_tasks": len(task_list)
    })

@app.route("/tasks/<int:id>", methods=["GET"])
def find_task(id):
    for task in tasks:
        if task.id == id:
            return jsonify(task.to_dict())
    return jsonify({
        "message": "Task not found"
    }), 404

@app.route("/tasks/<int:id>", methods=["PUT","PATCH"])
def update_task(id):
    task = None

    for t in tasks:
        if t.id == id:
            task = t
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    completed = data.get("completed")
    print(id, title, description, completed)

    if task is None:
        return jsonify({"message": "Task not found"}), 404
    
    task.title = title or task.title
    task.description = description or data.description
    task.completed = completed if completed is not None else task.completed 

    return jsonify(task.to_dict())

@app.route("/tasks/<int:id>", methods=["DELETE"])
def remove_task(id):
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            return jsonify(task.to_dict())
    
    return jsonify({ "mesage": "Task not found" }), 404
    
    

if __name__ == "__main__":
    app.run(debug=True)