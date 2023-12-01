"""GraphQL API to query the manga library"""
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, ObjectType
from database.database_connection import app
from database.queries import list_manga_records_resolver, get_manga_record_resolver
from database.mutations import create_manga_resolver, update_manga_resolver, delete_manga_resolver
from flask import jsonify, request

query = ObjectType("Query")
query.set_field("list_manga_records", list_manga_records_resolver)
query.set_field("get_manga_record", get_manga_record_resolver)

mutation = ObjectType("Mutation")
mutation.set_field("create_manga", create_manga_resolver)
mutation.set_field("update_manga", update_manga_resolver)
mutation.set_field("delete_manga", delete_manga_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(type_defs, query, mutation)

@app.route("/graphql", methods=["POST"])
def graphql_server():
    """GQL server for performing queries"""
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
    app.run(host='0.0.0.0', port=8080)
