# coding:UTF-8
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import bson

ADDR = "localhost"
PORT = 27017

def set():
    print("set")
    client = MongoClient(ADDR, PORT)
    db = client.test_database
    collection = db.test_collection
    post = {"author": "Mike","addr":"japan"}
    post_id = collection.insert_one(post).inserted_id
    print(post_id)
    print(db.list_collection_names())

def read():
    client = MongoClient(ADDR, PORT)
    db = client.test_database
    collection = db.test_collection
    cursor = collection.find({"author": "Mike"})
    for batch in cursor:
        print(bson.decode_all(batch))

def read_2():
    client = MongoClient(ADDR, PORT)
    db = client.test_database
    collection = db.test_collection
    for doc in collection.find({}):
        print(doc)


def set_2():
    client = MongoClient(ADDR, PORT)
    db = client.test_database
    collection = db.test_collection

    collection.update_one({"author":"Mike"},
    {"$set":{"email":"janedoe74@example2.com"}})

if "__main__" == __name__:
    set()



