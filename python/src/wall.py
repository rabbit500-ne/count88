from enum import Enum, auto
from pymongo import MongoClient

# **************************************************************
# DEFINE
# **************************************************************
ADDR = "localhost"
PORT = 27017

# **************************************************************
# scheme
# **************************************************************
class collection_tile_scheme():
    class _name() : pass
    class _doc():
        class _kifu():pass
        class _done():pass
        class _count():pass
        class _touch():pass

COLLECTION_TILE = {
    "name"    : None,
    "doc"     : {
        "kifu"    : None,
        "Done"    : None,
        "count"   : None,
        "touch"   : None
    }
}

COLLECTION_TILES = {
    "name"    : "tiles",
    "doc"     : {
        "LEVEL"   : None,
        "name"    : None,
        "parent"  : None,
        "Done"    : None,
    }
}

COLLECTION_PARAM = {
    "name"    : "param",
    "doc"     : {
        "count"   : None,
    }
}

# **************************************************************
# CODE
# **************************************************************
class Level(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()

def l_name( level:Level):
    print(level)
    return str(chr(level.value + 0x40))


class Tile():
    def __init__(self):
        self.parent = None
        self.level = None
        self.wall = None
        self.col_tiles = None
        self.col_tile = None
        self.name = None
        self.kifu = None
        pass

    def set_parent(self, parent):
        if self.name is None:
            return
        self.parent = parent
        tiles = self.wall.db[COLLECTION_TILES["name"]]
        tiles.update({"name" : self.name},{"$set", {"parent", parent}})

    def set_level(self, level):
        if self.name is None:
            return
        self.level = level
        tiles = self.wall.db[COLLECTION_TILES["name"]]
        tiles.update({"name" : self.name},{"$set", {"level", level}})

    def set_name(self, name):
        self.name = name
        tiles = self.wall.db[COLLECTION_TILES["name"]]
        tiles.insert({"name" : self.name})

    def set_param(self, parent, level, wall, kifu, records):
        if( (parent is not None) and (type(parent) is not Tile)):
            print("sdf")
            return False
        if( type(level) is not Level ):
            print("sqq")
            return False
        self.kifu = kifu

        self.parent = parent
        self.wall = wall
        self.level = level

        # collection 名　決める
        self.name = "t" + l_name( level ) + "_" + kifu
        print(self.name)

        self.col_tiles = self.wall.db[COLLECTION_TILES["name"]]
        self.col_tiles.insert({"name" : self.name})

        self.col_tile = self.wall.db[self.name]

    def insert(self,)
        
class Wall():
    def __init__(self):
        self.tiles = []
        self.client = None
        self.db = None
        self.w_param = None
        pass

    def set(self, db_name):
        self.client = MongoClient( \
            host=[ADDR + ":" + str(PORT)],\
            document_class=dict,\
            tz_aware=False,\
            connect=True)

        if db_name in self.client.database_names():
            print(self.client.database_names())
            pass
        else :
            raise Exception("データーベースがありません {0}".format(db_name))
        self.db = self.client[db_name]
        
        if COLLECTION_PARAM["name"] in self.db.collection_names():
            pass
        else:
            raise Exception("テーブルがありません {0}".format(COLLECTION_PARAM["name"] ))
        self.w_param = self.db[COLLECTION_PARAM["name"]]


    def build_tile( self, dic ):
        tile = Tile()
        if( not tile.set_param(wall=self, **dic) ):
            return False
        self.tiles.append(tile)
        
    def find_tile( self , col_name):
        return True
        
if __name__ == "__main__":
    wall = Wall();
    wall.set("test")
    # tile.set_param(parent=None,level=Level.A, wall=wall, kifu= "123", records=[1,2])
    dic = {"parent" : None,"level" : Level.A, "kifu": "123", "records":[1,2]}
    wall.build_tile(dic)



