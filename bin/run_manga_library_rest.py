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
from src.data import Data

app = Flask(__name__)
CORS(app)
host = HostEnum.LOCAL
logger = MangaLogger(host).register_logger(__name__)
data = Data(host)

@app.route('/get-library', methods=['GET'])
def get_library():
    '''
    Get the library data from the data layer and return it as a json response.
    
    Returns:
    - json: The library data as a json response.
    
    Raises:
    - FileNotFoundError: If any filepath could not be found.
    - Response: If there was an error getting the library data.
    - TypeError: The data type could not be determined.
    '''
    try:
        return jsonify({
            'volumes': data.get_volumes_data(),
            'series': data.get_series_data(),
            'shop': data.get_shop_data()
        })
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        logger.error(traceback.format_exc())
        logger.error('Failed to get library data')
        return Response('Failed to get library data... \n' + traceback.format_exc(), 500)

@app.route('/user-collection', methods=['GET'])
def get_collection():
    '''
    Get the user's collection data from the data layer and return it as a json response.
    
    Returns:
    - json: The collection data as a json response.
    
    Raises:
    - RequestException: If the request to the collection api fails.
    - JSONDecodeError: If the response contents from the api are not in a valid JSON format.
    '''
    try:
        user_id = request.args.get('user_id')
        return jsonify(data.get_collection_data(user_id))
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        logger.error('Failed to get collection data for %s', user_id)
        logger.error(traceback.format_exc())
        return Response('Failed to get collection data for ' + user_id + '... \n'
                        + traceback.format_exc(), 500)

@app.route('/add-collection', methods=['POST'])
def add_collection():
    '''
    Add a volume to the user's collection.
    
    Returns:
    - json: The collection data as a json response.
    
    Raises:
    - RequestException: If the request to the collection api fails.
    - JSONDecodeError: If the response contents from the api are not in a valid JSON format.
    '''
    try:
        return jsonify(data.add_to_collection_data(request.data))
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        logger.error('Failed to add to Collection: %s', json.dumps(request.data))
        logger.error(traceback.format_exc())
        return Response('Failed to add to Collection... \n' + traceback.format_exc(), 500)

@app.route('/delete-collection', methods=['POST'])
def delete_collection():
    '''
    Delete a volume from the user's collection.
    
    Returns:
    - json: The collection data as a json response.
    
    Raises:
    - RequestException: If the request to the collection api fails.
    - JSONDecodeError: If the response contents from the api are not in a valid JSON format.
    '''
    try:
        return jsonify(data.delete_from_collection_data(request.data))
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        logger.error('Failed to remove from Collection: %s', json.dumps(request.data))
        logger.error(traceback.format_exc())
        return Response('Failed to remove from Collection... \n' + traceback.format_exc(), 500)

@app.route('/user-wishlist', methods=['GET'])
def get_wishlist():
    '''
    Get the user's wishlist data from the data layer and return it as a json response.
    
    Returns:
    - json: The wishlist data as a json response.
    
    Raises:
    - RequestException: If the request to the wishlist api fails.
    - JSONDecodeError: If the response contents from the api are not in a valid JSON format.
    '''
    try:
        user_id = request.args.get('user_id')
        return jsonify(data.get_wishlist_data(user_id))
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        logger.error('Failed to get wishlist data for %s', user_id)
        logger.error(traceback.format_exc())
        return Response('Failed to get wishlist data for ' + user_id + '... \n'
                        + traceback.format_exc(), 500)

@app.route('/add-wishlist', methods=['POST'])
def add_wishlist():
    '''
    Add a volume to the user's wishlist.
    
    Returns:
    - json: The wishlist data as a json response.
    
    Raises:
    - RequestException: If the request to the wishlist api fails.
    - JSONDecodeError: If the response contents from the api are not in a valid JSON format.
    '''
    try:
        return jsonify(data.add_to_wishlist_data(request.data))
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        logger.error('Failed to add to Wishlist: %s', json.dumps(request.data))
        logger.error(traceback.format_exc())
        return Response('Failed to add to wishlist... \n' + traceback.format_exc(), 500)

@app.route('/delete-wishlist', methods=['POST'])
def delete_wishlist():
    '''
    Delete a volume from the user's wishlist.
    
    Returns:
    - json: The wishlist data as a json response.
    
    Raises:
    - RequestException: If the request to the wishlist api fails.
    - JSONDecodeError: If the response contents from the api are not in a valid JSON format.
    '''
    try:
        return jsonify(data.delete_from_wishlist_data(request.data))
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        logger.error('Failed to remove from Wishlist: %s', json.dumps(request.data))
        logger.error(traceback.format_exc())
        return Response('Failed to remove from Wishlist... \n' + traceback.format_exc(), 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050)
