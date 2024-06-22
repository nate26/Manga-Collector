'''
This is the main file for the manga library rest api. It is a flask app that serves as the backend
for the manga library web app. It is responsible for handling all the requests from the frontend
and interacting with the data layer to get the necessary data. It also handles the user collection
and wishlist data.
'''

import json
import traceback
from flask import Flask, jsonify, Response, request
from flask_cors import CORS
import requests
from src.enums.host_enum import HostEnum
from src.util.manga_logger import MangaLogger
from src.util.auth import Auth

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
CORS(app)

host = HostEnum.LOCAL
logger = MangaLogger(host).register_logger(__name__)
auth = Auth(host)

# print(auth.generate_token())

@app.route('/login', methods=['POST'])
def login():
    '''
    Login endpoint to generate a JWT token for the user
    '''
    try:
        return jsonify(request.data)
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        logger.error('Failed to generate a token %s', json.dumps(e))
        logger.error(traceback.format_exc())
        return Response('Failed to generate token... \n' + traceback.format_exc(), 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050)
