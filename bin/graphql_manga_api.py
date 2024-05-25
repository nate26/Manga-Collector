'''GraphQL API to query the manga library'''

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, ObjectType
from flask import Flask, jsonify, request
from flask_cors import CORS
from src.database.queries import Queries
from src.database.mutations import Mutations
from src.enums.host_enum import HostEnum
from src.util.manga_logger import MangaLogger

app = Flask(__name__)
CORS(app)
host = HostEnum.LOCAL
logger = MangaLogger(host).register_logger(__name__)
queries = Queries(host)
mutations = Mutations(host)


# Setup GQL resolvers

query = ObjectType('Query')
query.set_field('get_record', queries.get_record_resolver)
query.set_field('all_records', queries.all_records_resolver)
query.set_field('get_collection_series', queries.get_collection_series_resolver)

mutation = ObjectType('Mutation')
mutation.set_field('create_volume', mutations.create_volume_resolver)
mutation.set_field('update_volume', mutations.update_volume_resolver)
mutation.set_field('delete_volume', mutations.delete_volume_resolver)

type_defs = load_schema_from_path('schema.graphql')
schema = make_executable_schema(type_defs, query, mutation)


@app.route('/graphql', methods=['POST'])
def graphql_server():
    '''GQL server for performing queries'''
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
