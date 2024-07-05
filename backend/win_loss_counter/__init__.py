"""Module for serving the backend"""

import json
import logging
import pathlib
from urllib.parse import urlparse

import decouple
import flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send

_DEBUG = decouple.config("DEBUG", cast=bool, default=False)

MODULE_LOGGER = logging.getLogger(__name__)
MODULE_DIR = pathlib.Path(__file__).parent
FRONTEND_PATH = MODULE_DIR / ".." / ".." / "frontend" / "win-loss-counter"
DIST_PATH = (FRONTEND_PATH / "dist").resolve()

logging.warning("Dist path is: %s", DIST_PATH)

app = flask.Flask(__name__)

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

# region: web-server

@app.route("/", defaults={"path": "index.html"}, methods=["GET"])
def get_index(path):
    print("Handling root path")
    return flask.send_from_directory(DIST_PATH, path)


@app.route("/<path:path>", methods=["GET"])
def get_dir(path):
    parsed = urlparse(path).path
    print("Requested path is", path, "parsed to", parsed)
    if "." in parsed:
        return flask.send_from_directory(DIST_PATH, path)
    else:
        return flask.send_from_directory(DIST_PATH, "index.html")

# endregion
