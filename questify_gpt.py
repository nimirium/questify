import json
from typing import List

import openai
from dotenv import load_dotenv
import os

from models.task import Task

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def questify_tasks(tasks: List[Task]) -> dict:
    to_do = [t.model_dump() for t in tasks]
    prompt = "I have a list of tasks that I need to do. Turn each of them into a quest with a small storyline.\n\n" \
             + json.dumps(to_do) \
             + ' \n\n reply in a json format like \n' \
               '{"questlineName": "...", "quests": {"[id]": {"originalTask": "...", "questName": "...", "questDescription": "..."}}}' \
               'where [id] is the id of the task'
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[{
            "role": "user",
            "content": prompt,
        }]
    )
    return json.loads(completion["choices"][0]["message"]["content"])
