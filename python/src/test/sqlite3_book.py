# -*- coding: utf-8 -*-
import sqlite3

COUNT_BLOCKS = 6
COUNT_INT_MAX = 9223372036854775806
COUNT_TABLE_NAME = "param"
TARGET_TABLE_NAME = "param"

class Db_test():
    def __init__(self):
        self.con = sqlite3.connect(":memory:")
        self.cur = self.con.cursor()
        self.__kifu_count = [0] * COUNT_BLOCKS
        print(self.__kifu_count)

    def create(self):
        self.cur.execute("create table %s ("
            "kifu_count_0 INTEGER, kifu_count_1 INTEGER," "kifu_count_2 INTEGER, kifu_count_3 INTEGER," "kifu_count_4 INTEGER, kifu_count_5 INTEGER," "target_tile_name)" % COUNT_TABLE_NAME)
        self.cur.execute("insert into %s values (?, ?, ?, ?, ?, ?, ?)" % COUNT_TABLE_NAME, (0, 0, 0, 0, 0, 0,"0"))

    @property
    def kifu_count(self):
        self.cur.execute("select * from %s " % COUNT_TABLE_NAME)
        r = self.cur.fetchone()
        ret = 0
        for i in range(COUNT_BLOCKS):
            print("%d  %d" % (i,self.__kifu_count[i]))
            self.__kifu_count[i] = r[i]
            ret += self.__kifu_count[i] * (COUNT_INT_MAX ** i)
        return ret

    @kifu_count.setter
    def kifu_count(self,val):
        for i in reversed(range(COUNT_BLOCKS)):
            v = int(val / COUNT_INT_MAX ** i)
            self.__kifu_count[i] = v
            print(" set %d: " % i,self.__kifu_count[i])
            self.cur.execute("update %s set kifu_count_%d=? " % (COUNT_TABLE_NAME, i),(str(self.__kifu_count[i]),))
            val -= (COUNT_INT_MAX ** i) * v

    def kifu_incriment(self):
        for i in range(COUNT_BLOCKS):
            self.__kifu_count[i] += 1
            flg = self.__kifu_count[i] > COUNT_INT_MAX
            if flg:
                self.__kifu_count[i] = 0
            try:
                print("%d str(self.__kifu_count)" % i,str(self.__kifu_count))
                self.cur.execute("update %s set kifu_count_%d=? " % (COUNT_TABLE_NAME, i),(str(self.__kifu_count[i]),))
            except:
                print(self.__kifu_count)
                print(type(self.__kifu_count))
                raise

            if not flg:
                break

    @property
    def target_tile_name(self):
        self.cur.execute("select * from param ")
        r = self.cur.fetchone()
        self.__target_tile_name = r[1]
        return r[1]

    @target_tile_name.setter
    def target_tile_name(self,val):
        self.__target_tile_name = val
        self.cur.execute("update param set kifu_count=?", (str(val)))

    def get_target_data(self,tile_name):
        pass

    def run(self):
        self.create()
        print("S :",self.kifu_count)
        #9223372036854775807
        self.kifu_count = 9223372036854775806
        print("S2 :",self.kifu_count)
        self.kifu_incriment()
        self.kifu_incriment()
        self.kifu_incriment()
        print("s :", self.kifu_count)
        print("type",type(self.kifu_count))

def main():
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("create table lang (name ,first_appeared)")

    # This is the qmark style:
    cur.execute("insert into lang values (?, ?)", ("C", 1972))

    cur.execute("SELECT * FROM lang WHERE name=?", ("C")) 

if __name__ == '__main__':
    db_test = Db_test()
    db_test.run()