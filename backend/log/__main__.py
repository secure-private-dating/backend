from backend.model import get_db

from pymongo import MongoClient
import time
from pprint import pprint

client = MongoClient()
db = client['secure-private-dating']
last_message_id = None

while True:
    query = {}
    if last_message_id:
        query['_id'] = {'$gt': last_message_id}
    result = list(db.messages.find(query))
    for row in result:
        pprint(row)
        last_message_id = row['_id']
    time.sleep(1)
