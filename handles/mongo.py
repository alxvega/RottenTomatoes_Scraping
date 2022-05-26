from pymongo import MongoClient


def insert_bulk(lista_items, collection):
    with MongoClient('127.0.0.1', 27017) as client:
        db = client.scraping_project

        result = db[collection].bulk_write(lista_items)
        bulk_api_result = result.bulk_api_result
        print(f''
              f'Insert: {bulk_api_result["nUpserted"]} - '
              f'Matched:  {bulk_api_result["nMatched"]} - '
              f'Modified: {bulk_api_result["nModified"]}'
              )


def get_db_items(query, collection, project):
    with MongoClient('127.0.0.1', 27017) as client:
        db = client.scraping_project
        items = list(db[collection].find(query, project))

    return items
