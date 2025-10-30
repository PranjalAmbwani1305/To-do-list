from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# --- Initial To-Do list with 10 sample tasks ---
todos = [
    {"id": 1, "task": "Buy groceries", "done": False},
    {"id": 2, "task": "Finish Flask project", "done": False},
    {"id": 3, "task": "Clean the house", "done": True},
    {"id": 4, "task": "Pay electricity bill", "done": False},
    {"id": 5, "task": "Read a Python book", "done": False},
    {"id": 6, "task": "Workout for 30 minutes", "done": True},
    {"id": 7, "task": "Call Mom", "done": False},
    {"id": 8, "task": "Prepare for exam", "done": False},
    {"id": 9, "task": "Walk the dog", "done": True},
    {"id": 10, "task": "Plan weekend trip", "done": False}
]

# --- Helper functions ---
def add_task(task):
    todo = {"id": len(todos) + 1, "task": task, "done": False}
    todos.append(todo)
    return todo

def mark_done(task_id):
    for todo in todos:
        if todo["id"] == task_id:
            todo["done"] = True
            return todo
    return None

def delete_task(task_id):
    global todos
    todos = [t for t in todos if t["id"] != task_id]
    return todos


# --- Flask Routes ---
@app.route('/')
def home():
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>To-Do List</title>
        <style>
            body { font-family: Arial; background-color: #f2f2f2; margin: 30px; }
            h1 { text-align: center; color: #333; }
            table { width: 80%; margin: auto; border-collapse: collapse; background: white; }
            th, td { border: 1px solid #ccc; padding: 10px; text-align: center; }
            th { background-color: #4CAF50; color: white; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .done { color: green; font-weight: bold; }
            .pending { color: red; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>📋 To-Do List (Rendered by Python)</h1>
        <table>
            <tr>
                <th>ID</th>
                <th>Task</th>
                <th>Status</th>
            </tr>
            {% for todo in todos %}
            <tr>
                <td>{{ todo.id }}</td>
                <td>{{ todo.task }}</td>
                <td>
                    {% if todo.done %}
                        <span class="done">Done</span>
                    {% else %}
                        <span class="pending">Pending</span>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html_template, todos=todos)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(todos)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = data.get("task")
    if not task:
        return jsonify({"error": "Task name is required"}), 400
    new_task = add_task(task)
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    updated_task = mark_done(task_id)
    if updated_task:
        return jsonify(updated_task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def remove_task(task_id):
    delete_task(task_id)
    return jsonify({"message": f"Task {task_id} deleted."})


if __name__ == '__main__':
    app.run(debug=True)