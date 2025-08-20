"""
Rest API for managing login and sign-up for the site
"""

import json
import traceback
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import requests as req
from src.enums.host_enum import HostEnum
from src.util.manga_logger import MangaLogger
from src.util.auth import Auth

app = Flask(__name__)
CORS(app)

host = HostEnum.LOCAL
logger = MangaLogger(host).register_logger(__name__)
auth = Auth(host)

@app.route("/login", methods=["POST"])
def login():
    """
    Login endpoint to generate a JWT token for the user
    """
    try:
        body = json.loads(request.data)
        user_data = auth.login(body["email"], body["password"])
        return jsonify(user_data)
    except (req.exceptions.RequestException, json.JSONDecodeError) as e:
        logger.error("Failed to generate a token %s", json.dumps(e))
        logger.error(traceback.format_exc())
        return make_response({
            "message": "Failed to generate token... \n" + traceback.format_exc()
        }, 500)
    except ValueError as e:
        logger.error("Failed authenticate %s", e.args[0])
        logger.error(traceback.format_exc())
        return make_response({
            "message": e.args[0]
        }, 401, {"WWW-Authenticate": 'Basic realm="Login Required"'})

@app.route("/sign-up", methods=["POST"])
def signup():
    """
    Signup endpoint to create a new user
    """
    try:
        body = json.loads(request.data)
        user_data = auth.sign_up(body["email"], body["username"], body["password"])
        return jsonify(user_data)
    except (req.exceptions.RequestException, json.JSONDecodeError) as e:
        logger.error("Failed to create user %s", json.dumps(e))
        logger.error(traceback.format_exc())
        return make_response({
            "message": "Failed to create user... \n" + traceback.format_exc()
        }, 500)
    except ValueError as e:
        logger.error("Failed authenticate %s", e.args[0])
        logger.error(traceback.format_exc())
        return make_response({
            "message": e.args[0]
        }, 401, {"WWW-Authenticate": 'Basic realm="Login Required"'})

@app.route("/get-user-by-username", methods=["GET"])
def get_user_by_username():
    """
    Login endpoint to generate a JWT token for the user
    """
    try:
        username = request.args.get("username")
        if not username:
            raise ValueError("Username is required")
        user_data = auth.get_user(username)
        return jsonify(user_data)
    except (req.exceptions.RequestException, json.JSONDecodeError) as e:
        logger.error("Failed to get user data %s", json.dumps(e))
        logger.error(traceback.format_exc())
        return make_response({
            "message": "Failed to get user data... \n" + traceback.format_exc()
        }, 500)
    except ValueError as e:
        logger.error("Could not to find user by username %s", e.args[0])
        logger.error(traceback.format_exc())
        return make_response({
            "message": e.args[0]
        }, 401, {"WWW-Authenticate": 'Basic realm="Login Required"'})

@app.route("/refreshToken", methods=["POST"])
def refresh_token():
    """
    Refreshes the user's token. Requires a username and refresh_token in the body.
    """
    try:
        body = json.loads(request.data)
        auth_data = auth.refresh_token(body["username"], body["refresh_token"])
        return jsonify(auth_data)
    except (req.exceptions.RequestException, json.JSONDecodeError) as e:
        logger.error("Failed to generate a token %s", json.dumps(e))
        logger.error(traceback.format_exc())
        return make_response({
            "message": "Failed to generate token... \n" + traceback.format_exc()
        }, 500)
    except ValueError as e:
        logger.error("Failed authenticate %s", e.args[0])
        logger.error(traceback.format_exc())
        return make_response({
            "message": e.args[0]
        }, 401, {"WWW-Authenticate": 'Basic realm="Login Required"'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)
