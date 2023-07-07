from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from pydantic import ValidationError

from models.task import Task
from models.to_do_context import ToDoContext
from questify_gpt import questify_tasks

app = Flask(__name__)
limiter = Limiter(app, default_limits=["30/minute;500/day"])
CORS(app, resources={
    r"/questify": {
        "origins": ["http://localhost:*", "https://questify-to-do.vercel.app",
                    "http://questify-to-do.s3-website-us-east-1.amazonaws.com"]
    }
})


@app.route('/questify', methods=['POST'])
def questify():
    tasks_dicts = request.get_json()

    questify_task_data = []
    for task_dict in tasks_dicts:
        try:
            questify_task_data.append(Task(**task_dict))
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400

    result = questify_tasks(questify_task_data)
    return jsonify(result)


@app.route('/v2/questify', methods=['POST'])
def questify_v2():
    data = request.get_json()
    tasks_dicts = data.get('tasks')
    context_dict = data.get('context')

    if not tasks_dicts:
        return jsonify({"error": "No tasks provided"}), 400
    if not context_dict:
        return jsonify({"error": "No context provided"}), 400

    questify_task_data = []
    for task_dict in tasks_dicts:
        try:
            questify_task_data.append(Task(**task_dict))
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400

    context = None
    try:
        context = ToDoContext(**context_dict)
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    result = questify_tasks(tasks=questify_task_data, context=context)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
