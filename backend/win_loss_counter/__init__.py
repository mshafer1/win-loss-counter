"""Module for serving the backend"""

import functools
import json
import logging
import pathlib
import uuid
from urllib.parse import urlparse

import decouple
import flask
import flask_login
import flask_socketio
from flask_cors import CORS

_DEBUG = decouple.config("DEBUG", cast=bool, default=False)

MODULE_LOGGER = logging.getLogger(__name__)
MODULE_DIR = pathlib.Path(__file__).parent
FRONTEND_PATH = MODULE_DIR / ".." / ".." / "frontend" / "win-loss-counter"
DIST_PATH = (FRONTEND_PATH / "dist").resolve()

logging.warning("Dist path is: %s", DIST_PATH)

app = flask.Flask(__name__)

_login_manager = flask_login.LoginManager()
_login_manager.init_app(app)


class Score:
    def __init__(self):
        self.wins = self.losses = 0


class User(flask_login.UserMixin):
    def __init__(self, id_) -> None:
        super().__init__()
        self.id = id_


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

app.config["SECRET_KEY"] = decouple.config("FLASK_SECRET_KEY")
socketio = flask_socketio.SocketIO(app, **extra_socket_args)

_USERS = {}


@_login_manager.user_loader
def load_user(user_id):
    return _USERS.get(user_id)


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not flask_login.current_user.is_authenticated and not _DEBUG:
            print("User is not authenticated, closing connection")
            flask_socketio.disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped


@socketio.on("message")
def handle_message(data):
    print("received message: " + data)


@socketio.on("new score")
@authenticated_only
def handle_new_score(json_):
    data = json.loads(json_)
    print("received json: " + str(json_))
    _score.wins = data["wins"]
    _score.losses = data["losses"]
    flask_socketio.emit("newScore", dict(wins=_score.wins, losses=_score.losses), broadcast=True)


@socketio.on("connect")
def test_connect(auth):
    print("Connected")
    flask_socketio.emit("newScore", dict(wins=_score.wins, losses=_score.losses))


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
    if path == "control" and not flask_login.current_user.is_authenticated:
        print("User loaded control page and is not logged in. Assigning a uuid and logging in.")
        user_id = uuid.uuid4().hex
        user = User(user_id)
        _USERS[user_id] = user
        flask_login.login_user(user)
    if "." in parsed:
        return flask.send_from_directory(DIST_PATH, path)
    else:  # page routes like /control or / are handled via the frontend router in index.html
        return flask.send_from_directory(DIST_PATH, "index.html")


# endregion
