#------------------------------------------------
# deta base
#------------------------------------------------
import sqlite3
from dataclasses import dataclass
import ol_count
import ol_utils as util


LEVEL_THIN = [ 
    5, # LEVEL 0  
    5, # LEVEL 1  
    5, # LEVEL 2  
    5, # LEVEL 3  
    5, # LEVEL 4  
    5, # LEVEL 5  
]

PARAM_TABLE_NAME = "PARAM"
TILE_MANAGE_TABLE_NAME = "TILE_MANAGE"
TILE_TABLE_NAME = "TILE_%s_%s" # (level, kifu)

@dataclass
class PARAM_TABLESCHEMA():
    kifu_count : int = 0
    target_tile_name : str = ""

@dataclass
class TILE_MANAGE_TABLE_SCHEMA():
    level : bytes = 0
    name : str = "f" # Tile table name (kifu)
    parent_name : str = "f"
    parent_level : int = 0
    pointer : int = 0

@dataclass
class TILE_TABLE_SCHEMA():
    kifu : str = "1"
    count : int = 0
    done : bytes = 0

class Tile():
    def __init__(self):
        self.child_tiles = []

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, p):
        self.__parent = p

    @property
    def next_child_bord(self):
        bord = None
        player = None
        return (bord, player)
        

class Wall():
    def __init__(self):
        self.tiles = []

    def redy(self):
        self.read_db()
        self.read_tiles()
        # ALevel 読む
        self.redy_tile_A()
        # BLevel 読む
        # CLevel 読む
        # DLevel 読む
        # ELevel 読む
        # FLevel 読む

    def read_db(self):
        self.con = sqlite3.connect('example.db')
        self.cur = self.con.cursor()

    def read_tiles(self):
        pass

    def create_tile(self):
        pass

    def chk_tile(self):
        pass

    @property
    def target_tile_name(self):
        cmd = "SELECT * FROM ? WHERE "
        self.cur.execute(cmd, (PARAM_TABLE_NAME))
        r = self.cur.fetchone()
        return r['target_tile_name']

    @target_tile_name.setter
    def target_tile_name(self, tile):
        cmd = "UPDATE param SET target_tile_name=test WHERE "
        self.cur.execute(cmd)


    def redy_tile_A(self):
        pass





# マイグレード
# チェック系
# othello 計算処理以外
class kifuDB(Wall):
    def migrate(self):
        self.read_db()
        try:
            self.create_param_table()
        except sqlite3.OperationalError as e:
            pass
        self.create_tile_LEVEL_0()
        
    def create_param_table(self):
        self.create_table(PARAM_TABLE_NAME,PARAM_TABLESCHEMA())
        self.create_table(TILE_MANAGE_TABLE_NAME, TILE_MANAGE_TABLE_SCHEMA())
        # self.create_param_table(TILE_TABLE_SCHEMA())

    def create_table(self, table_name, schima):
        cmd = f"CREATE TABLE {table_name} "
        cmd += "("
        for key in schima.__dict__:
            cmd += key + " "
            if type(key) is str:
                cmd += "TEXT"
            elif type(key) is float:
                cmd += "REAL"
            elif type(key) is int:
                cmd += "INTEGER"
            elif type(key) is bytes:
                cmd += "BLOB"
            cmd += ", "
        cmd = cmd.rstrip(", ")
        cmd += ")"
        print("cmd", cmd)
        self.cur.execute(cmd)
        self.con.commit()

    def insert(self, table_name, schema):
        cmd = f"INSERT INTO {table_name} VALUES "
        cmd += "("
        for val in schema.__dict__.values():
            if type(val) is str:
                cmd += "'" + val + "'"
            else :
                cmd += f"{val}"
            cmd += ","
        cmd = cmd.rstrip(",")
        cmd += ")"
        print(" insert cmd, ",cmd)
        self.cur.execute(cmd)
        self.con.commit()


    def create_tile_LEVEL_0(self):
        parent_name = ""
        parent_level = 0
        name = 0
        level = 0
        tile_table_name = TILE_TABLE_NAME % (level, name)
        try:
            self.create_table( tile_table_name, TILE_TABLE_SCHEMA())
        except Exception:
            pass
        _bord = \
            """
            00000000
            00000000
            00000000
            000bw000
            000wb000
            00000000
            00000000
            00000000
            """
        bord = util.ConvStrBordToHexWB(_bord)
        player = util.BLACK
        kif_list = ol_count.run_Enumeration(bord, player, LEVEL_THIN[0])
        for kif in kif_list:
            row = TILE_TABLE_SCHEMA()
            row.kifu = self.conv(kif)
            self.insert(tile_table_name, row)

        # TODO parent などの設定。
        row = TILE_MANAGE_TABLE_SCHEMA()
        row.parent_level = parent_level
        row.parent_name = parent_name
        row.name = name
        row.level = level
        self.insert(TILE_MANAGE_TABLE_NAME, row)

        self.target_tile_name = name

    def conv(self,kif):
        return f"{kif[0][0]}_{kif[0][1]}_{kif[1]}_{kif[2]}"





