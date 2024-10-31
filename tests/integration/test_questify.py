import logging
import os
import sys
from typing import Dict

from pydantic import BaseModel, ValidationError

from models.task import Task

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from flask.testing import FlaskClient

from tests.fixtures.client import client


class Quest(BaseModel):
    originalTask: str
    questName: str
    questDescription: str


class ResponseModel(BaseModel):
    questlineName: str
    quests: Dict[str, Quest]


def test_questify(client: FlaskClient) -> None:
    response = client.post(
        "/questify", json=[{"id": "1", "text": "Test Task", "tags": []}]
    )
    assert response.status_code == 200
    try:
        ResponseModel(**response.get_json())
    except ValidationError as e:
        pytest.fail(f"Response structure did not match expected structure: {e}")


def test_questify_bad_request(client: FlaskClient) -> None:
    response = client.post(
        "/questify", json=[{"id": "1", "textz": "Test Task", "tags": []}]
    )
    assert response.status_code == 400
    logging.info(response.get_json())


def test_questify_v2_with_context(client: FlaskClient) -> None:
    response = client.post(
        "/v2/questify",
        json={
            "tasks": [{"id": "1", "text": "Hang the laundry", "tags": []}],
            "context": {
                "title": "Do these things before my baby wakes up",
                "time": "10:30 PM",
            },
        },
    )
    assert response.status_code == 200
    try:
        ResponseModel(**response.get_json())
        logging.info(response.get_json())
    except ValidationError as e:
        pytest.fail(f"Response structure did not match expected structure: {e}")


class GPTTasksResponse(BaseModel):
    message: str
    tasks: list[Task]


def test_gpt_tasks(client: FlaskClient) -> None:
    response = client.post(
        "http://127.0.0.1:5000/gpt-tasks",
        json={
            "tasks": [
                {"id": "123", "text": "Wash dishes", "is_completed": False, "tags": []},
                {
                    "id": "124",
                    "text": "Go to the store",
                    "is_completed": False,
                    "tags": [],
                },
            ],
            "message": "OK I'm done with the dishes.",
            "message_history": [],
        },
    )

    assert response.status_code == 200
    logging.info(response.get_json())
    result = GPTTasksResponse(**response.get_json())
    dishes_task = [task for task in result.tasks if task.id == "123"][0]
    assert dishes_task.is_completed is True
