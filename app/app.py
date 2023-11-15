from celery.result import AsyncResult
from flask import Flask, jsonify

from celery_app import celery

app = Flask(__name__)


@app.route("/")
def hello_world():
    print("hello world page")
    return "<p>Hello, World!</p>"


@app.route("/version")
def check_version():
    print("check version")
    res = {}
    with open("version", "r") as f:
        res = {"version": f.readline()}
    return jsonify(res)


@app.route("/add/<int:param1>/<int:param2>")
def add(param1: int, param2: int) -> str:
    task = celery.send_task("tasks.add", args=[param1, param2], kwargs={})
    response = f"<p>check status of {task.id} </p>"
    return response


@app.route("/result/add/<task_id>")
def add_result(task_id: str) -> str:
    res = AsyncResult(task_id, app=celery)
    print(res)
    if res.state == "SUCCESS":
        return f"<p>Result is : {res.result} </p>"
    else:
        return "<p>Please Wait.</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
