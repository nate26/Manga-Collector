'''
Rest API for managing login and sign-up for the site
'''

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

@app.route('/test', methods=['GET'])
def test():
    '''Test endpoint to check if the server is running'''
    authorization = request.headers.get('Authorization')
    if authorization:
        decoded = auth.decode_user(authorization.split(' ')[1])
        print(decoded)
        return jsonify(decoded)
    return jsonify({'message': 'This is only available with valid token'})

@app.route('/login', methods=['POST'])
def login():
    '''
    Login endpoint to generate a JWT token for the user
    '''
    try:
        body = json.loads(request.data)
        user_data = auth.login(body)
        return jsonify(user_data)
    except (req.exceptions.RequestException, json.JSONDecodeError) as e:
        logger.error('Failed to generate a token %s', json.dumps(e))
        logger.error(traceback.format_exc())
        return make_response({
            'message': 'Failed to generate token... \n' + traceback.format_exc()
        }, 500)
    except ValueError as e:
        logger.error('Failed authenticate %s', e.args[0])
        logger.error(traceback.format_exc())
        return make_response({
            'message': e.args[0]
        }, 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route('/sign-up', methods=['POST'])
def signup():
    '''
    Signup endpoint to create a new user
    '''
    try:
        body = json.loads(request.data)
        user_data = auth.sign_up(body)
        return jsonify(user_data)
    except (req.exceptions.RequestException, json.JSONDecodeError) as e:
        logger.error('Failed to create user %s', json.dumps(e))
        logger.error(traceback.format_exc())
        return make_response({
            'message': 'Failed to create user... \n' + traceback.format_exc()
        }, 500)
    except ValueError as e:
        logger.error('Failed authenticate %s', e.args[0])
        logger.error(traceback.format_exc())
        return make_response({
            'message': e.args[0]
        }, 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050)
