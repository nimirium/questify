from flask import Flask, request, jsonify
from flask_cors import CORS

from questify_gpt import questify_tasks

app = Flask(__name__)
# CORS(app, resources={r"/questify": {"origins": "http://localhost:port"}})
CORS(app)



@app.route('/questify', methods=['POST'])
def questify():
    tasks = request.get_json()
    questify_task_data = [{k: v for k, v in task.items() if k in ['id', 'text', 'tags']} for task in tasks]
    result = questify_tasks(questify_task_data)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
