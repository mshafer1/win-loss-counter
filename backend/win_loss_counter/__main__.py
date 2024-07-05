import json
import logging

import decouple
from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send

_DEBUG = decouple.config("DEBUG", cast=bool)

app = Flask(__name__)

class Score:
    def __init__(self):
        self.wins = self.losses = 0

_score = Score()

extra_socket_args = {}
if _DEBUG:
    logging.basicConfig(level=logging.DEBUG)
    logging.warning("enabling cross-origin-resource-loading")
    cors = CORS(app)
    extra_socket_args = {
        "cors_allowed_origins": "*",
        "logger": True,
        "enginio_logger": True,
    }

app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, **extra_socket_args)

@app.route("/")
def hellow_world():
    return "Hello..."

@socketio.on("message")
def handle_message(data):
    print("received message: " + data)


@socketio.on("new score")
def handle_new_score(json_):
    data = json.loads(json_)
    print("received json: " + str(json_), type(json_), data)
    _score.wins = data['wins']
    _score.losses = data['losses']
    emit("newScore", data, broadcast=True)


@socketio.on("connect")
def test_connect(auth):
    print("Connected")
    emit("newScore", dict(wins=_score.wins, losses=_score.losses))


@socketio.on("disconnect")
def test_disconnect():
    print("Client disconnected")


if __name__ == "__main__":
    socketio.run(app, debug=_DEBUG)
