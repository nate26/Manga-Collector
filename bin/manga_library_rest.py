import traceback
from flask import Flask, jsonify, Response, request
from flask_cors import CORS
from enums.host_enum import HostEnum
from util.manga_logger import MangaLogger
from src.data import Data
from src.user_data.collection import Collection

app = Flask(__name__)
CORS(app)
host = HostEnum.MOCK
logger = MangaLogger(host, __name__)
data = Data(host)
collection = Collection(host)

# todo, create log folder automatically on first load

@app.route('/get-library', methods=['GET'])
def get_library():
    try:
        return jsonify(data.get_library_data())
    except:
        logger.error('Failed to get library data', traceback.format_exc())
        return Response('Failed to get library data... \n' + traceback.format_exc(), 500)

@app.route('/user-collection', methods=['GET'])
def get_collection():
    try:
        user_id = request.args.get('user_id')
        return jsonify(collection.get_collection(user_id))
    except:
        logger.error('Failed to get collection data for ' + user_id, traceback.format_exc())
        return Response('Failed to get collection data for ' + user_id + '... \n' + traceback.format_exc(), 500)

@app.route('/add-collection', methods=['POST'])
def add_collection():
    try:
        return jsonify(data.add_to_collection_data(request.data))
    except:
        logger.warning('Collection save content:')
        logger.warning(request.data)
        logger.error('Failed to add to Collection', traceback.format_exc())
        return Response('Failed to add to Collection... \n' + traceback.format_exc(), 500)

@app.route('/delete-collection', methods=['POST'])
def delete_collection():
    try:
        return jsonify(data.delete_from_collection_data(request.data))
    except:
        logger.warning('Collection delete content:')
        logger.warning(request.data)
        logger.error('Failed to remove from Collection', traceback.format_exc())
        return Response('Failed to remove from Collection... \n' + traceback.format_exc(), 500)

@app.route('/user-wishlist', methods=['GET'])
def get_wishlist():
    try:
        user_id = request.args.get('user_id')
        return jsonify(data.get_wishlist_data(user_id))
    except:
        logger.error('Failed to get wishlist data for ' + user_id, traceback.format_exc())
        return Response('Failed to get wishlist data for ' + user_id + '... \n' + traceback.format_exc(), 500)

@app.route('/add-wishlist', methods=['POST'])
def add_wishlist():
    try:
        return jsonify(data.add_to_wishlist_data(request.data))
    except:
        logger.warning('Wishlist save content:')
        logger.warning(request.data)
        logger.error('Failed to add to wishlist', traceback.format_exc())
        return Response('Failed to add to wishlist... \n' + traceback.format_exc(), 500)

@app.route('/delete-wishlist', methods=['POST'])
def delete_wishlist():
    try:
        return jsonify(data.delete_from_wishlist_data(request.data))
    except:
        logger.warning('Wishlist delete content:')
        logger.warning(request.data)
        logger.error('Failed to remove from Wishlist', traceback.format_exc())
        return Response('Failed to remove from Wishlist... \n' + traceback.format_exc(), 500)


# api.add_resource(CreateRecord, '/create-record/')
# api.add_resource(EnrichFromMal, '/enrich-from-mal/')
# api.add_resource(OverrideRecord, '/override-record/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050)