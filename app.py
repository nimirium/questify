from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import ValidationError

from models.task import Task
from questify_gpt import questify_tasks

app = Flask(__name__)
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


if __name__ == '__main__':
    app.run(debug=True)
