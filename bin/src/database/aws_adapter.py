from datetime import datetime, timedelta
from typing import List
import requests
from src.interfaces.icollection import ICollection
from src.enums.file_path_enum import FilePathEnum
from src.enums.host_enum import HostEnum
from src.util.local_dao import LocalDAO
from src.util.manga_logger import MangaLogger

class AWSAdapter:

    def __init__(self, host: HostEnum) -> None:
        self.logger = MangaLogger(host).register_logger(__name__)
        self.session = requests.Session()
        vault = LocalDAO(host).open_file(FilePathEnum.VAULT.value[host.value])
        self.collection_host = vault['aws_collection_host']
        self.collection_api_key = vault['aws_collection_api_key']


    def get_collection_data(self, user_id: str) -> List[ICollection]:
        """
        Gets the data from the AWS directory
        
        Parameters
        ----------
        user_id : str
            The user_id to get the data from
        
        Returns
        -------
        List[ICollection]
            The data from the AWS directory
        
        Raises
        ------
        JSONDecodeError:
            If the response contents from AWS are not in a valid JSON format.
        RequestException:
            If the get request to AWS fails
        """
        start = datetime.now()

        graphql_query = """{
            listMangaUserCollections(filter: { user_id: { eq: "%s" } }) {
                items {
                    id
                    user_id
                    cost
                    giftToMe
                    purchaseDate
                    isbn
                    merchant
                    read
                    tags
                    state
                    inserted
                    updated
                }
            }
        }""" % user_id

        response = self.session.request(
            url = 'https://' + self.collection_host + '/graphql',
            method = 'POST',
            json = { 'query': graphql_query },
            headers = {
                'Content-type': 'application/graphql', 
                'x-api-key': self.collection_api_key,
                'host': self.collection_host
            }
        )

        end = (datetime.now() - start).total_seconds()
        self.logger.info('Time to get data from AWS: %s', str(timedelta(seconds=end)))

        # catch error cases
        # add try / except block

        return response.json()['data']['listMangaUserCollections']['items']





















    #     try:
    #         start = datetime.now()
    #         response = requests.get(url, timeout=30).json()
    #         end = (datetime.now() - start).total_seconds()
    #         self.logger.info('Time to get data from AWS: %s', str(timedelta(seconds=end)))
    #         return response
    #     except (json.JSONDecodeError, requests.exceptions.RequestException):
    #         self.logger.error(traceback.format_exc())
    #         self.logger.error('Could not get data from %s ... ending process', url)
    #         raise


    # def get_user_list(self, user_id: str) -> List[ICollection]:
    #     try:
    #         result = self.table.scan(FilterExpression=Attr('user_id').eq(user_id))
    #         items = result.get("Items")
    #         self.logger.info(items)
    #         return items #json.dumps(, cls=DecimalEncoder)
    #     except ClientError as err:
    #         raise ClientError(json.dumps("Error getting data from the database :: " + str(err)))
            
            
    # def ddb_put_item(table, record):
    #     record["updated"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    #     table.put_item(Item=record)


    # def modify_records(records, table):
    #     try:
    #         records_insert, records_update, insert_results = [], [], []
    #         for r in records:
    #             (records_insert, records_update)["id" in r.keys()].append(r)
    #         if len(records_update) > 0:
    #             update_records(records_update, table)
    #         if len(records_insert) > 0:
    #             insert_results = add_records(records_insert, table)
    #         results = [r if 'id' in r else insert_results.pop(0) for r in records]
    #         return {
    #             'statusCode': 200,
    #             'headers': cors_headers,
    #             'body': json.dumps(results, cls=DecimalEncoder)
    #         }
    #     except ClientError as err:
    #         return {
    #             'statusCode': 500,
    #             'headers': cors_headers,
    #             'body': json.dumps("Error saving to the database :: " + str(err))
    #         }
    #     except AttributeError as err:
    #         return {
    #             'statusCode': 400,
    #             'headers': cors_headers,
    #             'body': json.dumps(err)
    #         }


    # def add_records(records, table):
    #     if all(all(elem in record for elem in ("user_id", "isbn", "state", "purchaseDate", "cost", "merchant", "giftToMe", "read", "tags")) for record in records):
    #         formatted_records = [{
    #             "id": str(uuid.uuid4()),
    #             "user_id": record.get("user_id"),
    #             "isbn": record.get("isbn"),
    #             "state": record.get("state"),
    #             "purchaseDate": record.get("purchaseDate"),
    #             "cost": record.get("cost"),
    #             "merchant": record.get("merchant"),
    #             "giftToMe": record.get("giftToMe"),
    #             "read": record.get("read"),
    #             "tags": record.get("tags"),
    #             "inserted": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
    #             "updated": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    #         } for record in records]
    #         try:
    #             if len(formatted_records) == 1:
    #                 ddb_put_item(table, formatted_records[0])
    #             else:
    #                 with table.batch_writer() as table_writer:
    #                     for formatted_record in formatted_records:
    #                         ddb_put_item(table_writer, formatted_record)
    #         except ClientError as err:
    #             raise err
    #         return formatted_records
    #     else:
    #         raise AttributeError('Incorrect attributes on records...')
            
            
    # def ddb_update_item(table, record):
    #     table.update_item(
    #         Key={ 'id': record.get("id"), 'user_id': record.get("user_id") },
    #         UpdateExpression='SET state= :stt, purchaseDate= :purchaseDate, cost= :cost, merchant= :merchant, giftToMe= :giftToMe, read= :read, updated= :updated',
    #         ExpressionAttributeValues={
    #             ':stt': record.get("state"),
    #             ':purchaseDate': record.get("purchaseDate"),
    #             ':cost': record.get("cost"),
    #             ':merchant': record.get("merchant"),
    #             ':giftToMe': record.get("giftToMe"),
    #             ':read': record.get("read"),
    #             ':updated': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    #         }
    #     )


    # def update_records(records, table):
    #     if all(all(elem in record for elem in ("id", "user_id", "isbn", "state", "purchaseDate", "cost", "merchant", "giftToMe", "read", "tags")) for record in records):
    #         try:
    #             if len(records) == 1:
    #                 # ddb_update_item(table, records[0])
    #                 ddb_put_item(table, records[0])
    #             else:
    #                 with table.batch_writer() as table_writer:
    #                     for record in records:
    #                         ddb_put_item(table_writer, record)
    #         except ClientError as err:
    #             raise err
    #         return records
    #     else:
    #         raise AttributeError('Incorrect attributes on records...')
            
            
    # def ddb_delete_item(table, record):
    #     table.delete_item(Key={ 'id': record.get("id"), 'user_id': record.get("user_id") })
            
            
    # def delete_records(records, table):
    #     if all(all(elem in record for elem in ("id", "user_id")) for record in records):
    #         try:
    #             if len(records) == 1:
    #                 ddb_delete_item(table, records[0])
    #             else:
    #                 with table.batch_writer() as table_writer:
    #                     for record in records:
    #                         ddb_delete_item(table_writer, record)
    #         except ClientError as err:
    #             return {
    #                 'statusCode': 500,
    #                 'headers': cors_headers,
    #                 'body': json.dumps("Error deleting records from the database :: " + str(err))
    #             }
    #         return {
    #             'statusCode': 200,
    #             'headers': cors_headers,
    #             'body': json.dumps("Deleted records from collection db: " + json.dumps(records))
    #         }
    #     else:
    #         return {
    #             'statusCode': 400,
    #             'headers': cors_headers,
    #             'body': json.dumps("Incorrect attributes on record ids...")
    #         }
        

    # def lambda_handler(event, context):
    #     dyn_resource = boto3.resource('dynamodb')
    #     table = dyn_resource.Table('manga_user_collection')
        
    #     result = {
    #         'statusCode': 404,
    #         'headers': cors_headers,
    #         'body': json.dumps("Functionality not yet implemented!")
    #     }
        
    #     if event.get("resource") == "/user-records":
    #         result = get_user_list(event.get("queryStringParameters"), table)
    #     elif event.get("resource") == "/add-records":
    #         records = json.loads(event.get("body"), parse_float=Decimal)
    #         result = modify_records(records, table)
    #     elif event.get("resource") == "/delete-records":
    #         records = json.loads(event.get("body"))
    #         result = delete_records(records, table)

        
    #     return result
