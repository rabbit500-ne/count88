import sys
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from wall import Wall, Level

from datetime import datetime
user_doc = {
    "username" : "janedoe",
    "firstname" : "Jane",
    "surname" : "Doe",
    "dateofbirth" : datetime(1974, 4, 12),
    "email" : "janedoe74@example.com",
    "score" : 0
}

print(user_doc["dateofbirth"])

def build_wall_t_01():
    w01 = Wall();
    w01.set(db_name = "test")
    kifu_dic = {
        "kifu": "aaaa"
        "count": 0
    }

    tile_dic = {
        "parent" : None,
        "level" : Level.A
        "records" : None
        "name" : None}
    w01.build_tile(tile_dic)

def test_main():
    try:
        c = MongoClient( \
            host=['localhost:27017'],\
            document_class=dict,\
            tz_aware=False,\
            connect=True)
        print("接続に成功しました")
    except ConnectionFailure as e:
        sys.stderr.write("MongoDBへ接続できません: %s" % e)
    db = c["test"]
    col = db["test"]
    doc = col.find_one()
    print(doc["name"])
    

if __name__ == "__main__":
    build_wall_t_01()