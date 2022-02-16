#------------------------------------------------
# deta base
#------------------------------------------------
import dataclasses
import sqlite3
from dataclasses import dataclass
import ol_count
import ol_utils as util
from ol_utils import BORD_WB, PLAYER
from typing import List,Dict


class ExceptionChiledOver(Exception):pass
class LONG_INT(int):pass

LEVEL_THIN = [ 
    5, # LEVEL 0  
    5, # LEVEL 1  
    5, # LEVEL 2  
    5, # LEVEL 3  
    5, # LEVEL 4  
    5, # LEVEL 5  
    5, # LEVEL 6  
    5, # LEVEL 7  
    5, # LEVEL 8  
    5, # LEVEL 9  
    5, # LEVEL 10  
    5, # LEVEL 11  
    5, # LEVEL 12  
    5, # LEVEL 13  
    5, # LEVEL 14  
    5, # LEVEL 15  
    5, # LEVEL 16  
    5, # LEVEL 17  
    5, # LEVEL 18  
    5, # LEVEL 19  
    5, # LEVEL 20

]

PARAM_TABLE_NAME = "PARAM"
TILE_MANAGE_TABLE_NAME = "TILE_MANAGE"
TILE_TABLE_NAME = "t%s" # (kifu)

INMEMORY = './20220211_1200.data'
DB_FILE = INMEMORY
i = 0

@dataclass
class User:
    name: str
    age: int = 0

@dataclass
class PARAM_TABLESCHEMA:
    kifu_count : LONG_INT = 0
    target_tile_name : str = ""

@dataclass
class TILE_MANAGE_TABLE_SCHEMA:
    level : bytes = 0
    name : str = "f" # Tile table name (kifu)
    parent_name : str = "f"
    parent_level : int = 0
    pointer : int = 0
    duplication : int = 1

@dataclass
class TILE_TABLE_SCHEMA:
    kifu : str = ""
    level : int = 0
    count : int = 0
    done : bytes = 0
    pointer : int = 0
    duplication : int = 1

# class Tile():
#     def __init__(self):
#         self.child_tiles = []

#     @property
#     def parent(self):
#         return self.__parent

#     @parent.setter
#     def parent(self, p):
#         self.__parent = p

#     @property
#     def next_child_bord(self):
#         bord = None
#         player = None
#         return (bord, player)
        
COUNT_BLOCKS = 6
COUNT_INT_MAX = 9223372036854775806
COUNT_TABLE_NAME = "param"
TARGET_TABLE_NAME = "param"

class dbi():
    def __init__(self, con):
        self.con = con
        self.cur = self.con.cursor()

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
            elif type(key) is LONG_INT:
                cmd += "TEXT"
            cmd += ", "
        cmd = cmd.rstrip(", ")
        cmd += ")"
        print("cmd", cmd)
        try:
            self.cur.execute(cmd)
        except sqlite3.OperationalError:
            print("sqlite3. Error!")
            raise

        
        # self.cur.commit() # ???

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
        cmd += ");"
        print(" insert cmd, ",cmd)
        self.cur.execute(cmd)
        # self.con.commit() ???

    def save(self):
        self.con.commit()

    def update(self, table_name, select_field, select_value, field, value):
        pass

class Tile(dbi):
    def __init__(self, con):
        # read時、create時ある。
        super().__init__(con)
        self.wood = None
        self.wall = None
        self.curr_tile = None

    def read(self,kif:util.Kif):
        self.kif = kif
        # self.wood = wood

        # cmd = f"SELECT * FROM {self.table_name};"
        # print(cmd)
        # self.cur.execute(cmd)
        # chiled = self.cur.fetchall()
        # if chiled is None:
        #     return
        # print(f"len {len(chiled)}")
        pass

    def read_chiled_tiles(self):
        cmd = f"SELECT kifu FROM {self.table_name};"
        print(cmd)
        print("-_0  " +self.kif.name)
        self.cur.execute(cmd)
        children = self.cur.fetchall()
        child_tile : List(Tile) = []
        print("-_1  " +self.kif.name)
        for chiled in children:
            kif = util.Kif(
                bord=BORD_WB(
                    w=0,
                    b=0
                ),
                pas=0,
                player=None,
            )
            kif.name = chiled[0]
            # print("-_  " + chiled[0] + " " +self.kif.name + " " + str(type(kif)))
            ch_tile = Tile(self.con)
            ch_tile.kif = kif
            ch_tile.parent = self
            child_tile.append(ch_tile)
        self.__chiled_tiles = child_tile
        print("-_2  " +self.kif.name)


    def create(self,parent,kif, wood, level, duplication):
        # 新しく作る場合
        self.duplication = duplication
        self.__kif = kif
        self.__parent = parent
        self.wood = wood
        self.__level = level
        self.__pointer = 0
        self.done = False        

    @property
    def kif(self):
        return self.__kif

    @kif.setter
    def kif(self, val : util.Kif):
        self.__kif = val

    @property
    def table_name(self):
        return TILE_TABLE_NAME % self.kif.name

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self,tile):
        self.__parent = tile
        # db 操作
        #self.update(TILE_MANAGE_TABLE_NAME,"name",self.table_name,"parent",tile.table_name)

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, level):
        self.__level = level
        # db 操作
        self.update(self.parent.table_name,"kifu_name",self.kif.name,"level",level)

    @property
    def pointer(self):
        try:
            return self.__pointer
        except AttributeError as e:
            print(e)
            pass
        cmd = f"SELECT pointer FROM {self.parent.table_name} WHERE kifu='{self.kif.name}';"
        print(cmd)
        self.cur.execute(cmd)
        r = self.cur.fetchone()
        print(r)
        self.__pointer = int(r[0])
        return self.__pointer

    @pointer.setter
    def pointer(self, val):
        self.__pointer = val
        self.update(self.parent.table_name,"kifu",self.kif.name,"pointer",val)

    @property
    def duplication(self):
        return self.__duplication

    @duplication.setter
    def duplication(self, val):
        self.__duplication = val

    @property
    def chiled_tiles(self):
        try:
            return self.__chiled_tiles
        except AttributeError as e:
            print(e)
        self.read_chiled_tiles()
        return self.__chiled_tiles
        

    @chiled_tiles.setter
    def chiled_tiles(self,chiled_tiles):
        self.__chiled_tiles = chiled_tiles
        # db 操作
        try:
            row = TILE_TABLE_SCHEMA()
            row.level = self.__level
            row.kifu = self.kif.name
            row.pointer = self.__pointer
            row.duplication = self.duplication
            self.create_table(self.table_name, row)
            # self.create_table(self.table_name,TILE_TABLE_SCHEMA())
        except sqlite3.OperationalError:
            raise sqlite3.OperationalError
        
        for tile in chiled_tiles:
            schima = TILE_TABLE_SCHEMA()
            schima.kifu = tile.kif.name
            self.insert(self.table_name, schima)
        self.save()

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self, count):
        self.__count = count
        # db 
        # table = TILE_TABLE_NAME % (self.parent.level, self.parent.name)
        self.update(self.parent.table_name, "kif", self.kif.name, "count", count)

        self.wood.kifu_count_plus( count) # TODO 速度要検討

    @property
    def chiled_count(self):
        count = 0
        for tile in self.chiled_tiles:
            count += tile.count
        return count

    def cullent_chiled(self):
        try:
            tile = self.chiled_tiles[self.pointer]
            if tile.done:
                print(f"done :{tile.done}")
                self.pointer += 1
                tile = self.cullent_chiled()
        except ExceptionChiledOver:
            print("error  ExceptionChiledOver:")
            self.done = True
            self.count = self.chiled_count
            raise ExceptionChiledOver
        return tile

    @property
    def done(self):
        try:
            return self.__done
        except AttributeError as e:
            print(f" done error   :{e}")
        cmd = f"SELECT done FROM {self.parent.table_name} WHERE kifu='{self.kif.name}';"
        self.cur.execute(cmd)
        ret = self.cur.fetchone()
        self.__done = bytes(int(ret[0]))
        return self.__done

    @done.setter
    def done(self, val:bool):
        self.__done = val


    # def next_chiled(self):
    #     try :
    #         tile = self.__chiled_tiles[self.pointer + 1]
    #         if tile.done is True:
    #             self.pointer += 1
    #             self.next_chiled()
    #     except:
    #         print("chiled over.")

    #         raise Exception()
    #     self.pointer += 1
    #     return tile

    def create_chiled(self):
        # kif = self.kif
        # bord = kif.bord
        # player = kif.player
        kif_list = ol_count.run_Enumeration(self.kif, LEVEL_THIN[self.level + 1])
        if self.is_all_end(kif_list):
            self.count = len(kif_list)
            self.done = True
            raise ExceptionChiledOver
        chiled_tiles = []
        d_dict = self.duplication_list(kif_list)
        for data in d_dict.values():
            # print(f"   {data}")
            ct = Tile(self.con)
            try:
                ct.create(self, data.kif, self.wood, self.level+1, data.duplication)
            except:
                raise sqlite3.OperationalError

            chiled_tiles.append(ct)
        self.chiled_tiles = chiled_tiles
        self.save()

    def is_all_end(self,kif_list):
        for kif in kif_list:
            if kif.pas < 2:
                return False
        return True

    def duplication_list(self, k_list : List[util.Kif]):
        @dataclasses.dataclass
        class data():
            duplication : int
            kif : util.Kif
        unique_dict : Dict[data] = {}
        for kif in k_list:
            if unique_dict.get(kif.name) is None:
                unique_dict[kif.name] = data(duplication=1,kif = kif)
            else:
                unique_dict[kif.name].duplication += 1

        return unique_dict

class Wood(dbi):
    def create(self):
        self.create_param_table()
        self.__kifu_count = 0
        self.kifu_count_plus(0)

    def create_param_table(self):
        self.create_table(PARAM_TABLE_NAME,PARAM_TABLESCHEMA())
        # self.create_table(TILE_MANAGE_TABLE_NAME, TILE_MANAGE_TABLE_SCHEMA())
        # self.create_param_table(TILE_TABLE_SCHEMA())
    
    @property
    def kifu_count(self):
        self.cur.execute("select kifu_count from %s " % COUNT_TABLE_NAME)
        r = self.cur.fetchone()
        self.__kifu_count = LONG_INT(r[0])
        return LONG_INT(r[0])

    def kifu_count_plus(self,val):
        self.__kifu_count += val
        self.cur.execute("update %s set kifu_count=?"% COUNT_TABLE_NAME , ( str(self.__kifu_count)))
        self.con.commit()

    # @property
    # def kifu_count(self):
    #     self.cur.execute("select * from %s " % COUNT_TABLE_NAME)
    #     r = self.cur.fetchone()
    #     ret = 0
    #     for i in range(COUNT_BLOCKS):
    #         print("%d  %d" % (i,self.__kifu_count[i]))
    #         self.__kifu_count[i] = r[i]
    #         ret += self.__kifu_count[i] * (COUNT_INT_MAX ** i)
    #     return ret

    # @kifu_count.setter
    # def kifu_count(self,val):
    #     for i in reversed(range(COUNT_BLOCKS)):
    #         v = int(val / COUNT_INT_MAX ** i)
    #         self.__kifu_count[i] = v
    #         print(" set %d: " % i,self.__kifu_count[i])
    #         self.cur.execute("update %s set kifu_count_%d=? " % (COUNT_TABLE_NAME, i),(str(self.__kifu_count[i]),))
    #         val -= (COUNT_INT_MAX ** i) * v
    #     self.con.commit()

    # def kifu_incriment(self):
    #     for i in range(COUNT_BLOCKS):
    #         self.__kifu_count[i] += 1
    #         flg = self.__kifu_count[i] > COUNT_INT_MAX
    #         if flg:
    #             self.__kifu_count[i] = 0
    #         try:
    #             print("%d str(self.__kifu_count)" % i,str(self.__kifu_count))
    #             self.con.cursor.execute("update %s set kifu_count_%d=? " % (COUNT_TABLE_NAME, i),(str(self.__kifu_count[i]),))
    #         except:
    #             print(self.__kifu_count)
    #             print(type(self.__kifu_count))
    #             raise

    #         if not flg:
    #             break

class wall():
    def __init__(self):
        self.con = sqlite3.connect(DB_FILE)
        self.cur = self.con.cursor()     

    def create_wood(self):
        self.wood = Wood(self.con)
        self.wood.create()

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
        cmd = "UPDATE %s SET target_tile_name=%s WHERE " % (PARAM_TABLE_NAME, tile)
        self.cur.execute(cmd)

    def target_tile_pointer(self, tile_name):
        cmd = f'SLECET * FROM {TILE_MANAGE_TABLE_NAME} WHERE name=:name'
        self.cur.execute(cmd, {"name":tile_name})
        r = self.cur.fetchone()
        return r['pointer']


    def redy_tile_0(self):
        # TILE_MANAGE_TABLE からlevel0を読む
        pass

    @property
    def target_kifu(self):
        pointer = self.target_tile_pointer(self.target_tile_name)
        cmd = "SELECT * FROM %s WHERE id=:id" % self.target_tile_name # TODO NOW
        self.cur.execute(cmd, {"id": pointer})
        r = self.cur.fetchone()
        return r['kifu']

class wall_reader(wall):
    def read(self):
        # _bord = \
        #     """
        #     00000000
        #     00000000
        #     00000000
        #     000bw000
        #     000wb000
        #     00000000
        #     00000000
        #     00000000
        #     """
        # [b,w] = util.ConvStrBordToHexWB(_bord)
        kif = util.Kif(
            bord = util.BORD_WB(
                b=0,
                w=0
            ),
            pas=0,
            player=util.PLAYER.black
        )
        self.target_tile = Tile(self.con) #t0_0_0_0 table
        self.target_tile.kif = kif

        self.target_tile.read_chiled_tiles()
        print(f"1-->{self.target_tile.table_name}")

        self.target_tile = self.target_tile.chiled_tiles[0]
        print(f"2-->{self.target_tile.table_name}")

        #TODO pointerのread.

        self.target_tile.read_chiled_tiles()
        print(f"3-->{self.target_tile.table_name}")
        self.target_tile = self.target_tile.cullent_chiled()


        # self.read_tiles()
        # ALevel 読む
        # self.redy_tile_0()
        # BLevel 読む
        # CLevel 読む
        # DLevel 読む
        # ELevel 読む
        # FLevel 読む   

class Wall_if():
    def get_kifu(self):
        pass

    def set_count(self, kifu, count):
        pass

class wall_sheeder(wall):
    def start(self):
        # self.read_db()
        self.create_wood()
        self.sheeder_tile_LEVEL_0() #0
        self.sheeder_tile_LEVEL_X() #1
        self.sheeder_tile_LEVEL_X() #2
        self.sheeder_tile_LEVEL_X() #3
        self.sheeder_tile_LEVEL_X() #4
        self.sheeder_tile_LEVEL_X() #5

        self.sheeder_tile_LEVEL_X() #6
        self.sheeder_tile_LEVEL_X() #7
        self.sheeder_tile_LEVEL_X() #8
        self.sheeder_tile_LEVEL_X() #9
        self.sheeder_tile_LEVEL_X() #10
        self.sheeder_tile_LEVEL_X() #11
        self.sheeder_tile_LEVEL_X() #12
        self.sheeder_tile_LEVEL_X() #13
        self.sheeder_tile_LEVEL_X() #14
        # self.sheeder_tile_LEVEL_X() #15
        # self.sheeder_tile_LEVEL_X() #16
        # self.sheeder_tile_LEVEL_X() #17
        # self.sheeder_tile_LEVEL_X() #18
        # self.sheeder_tile_LEVEL_X() #19

    def sheeder_tile_LEVEL_0(self):
        brank_tile =Tile(self.con)
        brank_kif = util.Kif(
            bord= BORD_WB(
                b=0,
                w=0
            ),
            pas=0,
            player=PLAYER.black
        )

        # db = dbi(self.con)
        # db.create_table(TILE_TABLE_NAME % brank_kif.name, TILE_TABLE_SCHEMA())
        brank_tile.create(None, brank_kif, self.wood, 0, 1)
        # brank_tile.__kif = brank_kif
        # brank_tile.__level = 0
        # brank_tile.__pointer = 0
        # brank_tile.wood = self.wood
        # brank_tile.__duplication = 1

        tile = Tile(self.con)
        # TODO brank_tile のセット
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
        [b,w] = util.ConvStrBordToHexWB(_bord)
        kif = util.Kif(
            bord= BORD_WB(
                b=b,
                w=w
            ),
            pas=0,
            player=PLAYER.black
        )
        tile.create(brank_tile,kif, self.wood, 0, 1)
        brank_tile.chiled_tiles=[tile]
        tile.create_chiled()
        self.target_tile = tile

    def sheeder_tile_LEVEL_X(self):
        tile = self.target_tile.cullent_chiled()
        tile.create_chiled()
        self.target_tile = tile

    # def convKifuName(self,kif):
    #     """
    #     kif[0][0] : black bord
    #     kif[0][1] : white bord
    #     kif[1] : pass count
    #     kif[2] : player
    #     """
    #     return f"{kif[0][0]}_{kif[0][1]}_{kif[1]}_{kif[2]}"





