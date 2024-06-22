'''
This is the main file for the manga library rest api. It is a flask app that serves as the backend
for the manga library web app. It is responsible for handling all the requests from the frontend
and interacting with the data layer to get the necessary data. It also handles the user collection
and wishlist data.
'''

from functools import wraps
import json
import traceback
from flask import Flask, jsonify, Response, request, session, make_response
from flask_cors import CORS
import requests
from src.enums.host_enum import HostEnum
from src.util.manga_logger import MangaLogger
from src.util.auth import Auth

app = Flask(__name__)
CORS(app)

host = HostEnum.LOCAL
logger = MangaLogger(host).register_logger(__name__)
auth = Auth(host)

# print(auth.generate_token())

# def token_required(func):
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         token = request.args.get('token')
#         if not token:
#             return jsonify({'message': 'Token is missing'}), 403
#         try:
#             data = auth.decode(token, app.config['SECRET_KEY'])
#         except:
#             return jsonify({'message': 'Token is invalid'}), 403
#         return decorated

# @app.route('/test', methods=['GET'])
# @token_required
# def test():
#     return jsonify({'message': 'This is only available with valid token'})

@app.route('/login', methods=['POST'])
def login():
    '''
    Login endpoint to generate a JWT token for the user
    '''
    try:
        body = json.loads(request.data)
        if body['username'] and body['password']:
            token = auth.encode(body, app.config['SECRET_KEY'])
            print(token)
            return jsonify({'token': token})
        else:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(e)
        logger.error('Failed to generate a token %s', json.dumps(e))
        logger.error(traceback.format_exc())
        return make_response('Failed to generate token... \n' + traceback.format_exc(), 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050)
