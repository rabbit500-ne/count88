
#------------------------------------------------
# 統計管理
#------------------------------------------------
# class Db 依存

import threading
import wall2 as Wall
import time
import ol_count

class ExceptEnd(Exception):pass

class Root():
    def __init__(self):
        self.wall = Wall.wall_reader()
        pass

    def redy(self):
        # DB にアクセス
        # DBがすでにあることが前提
        self.wall.read()
        self.target_tile = self.wall.target_tile
        self.next_target_tile = self.next_tile(self.target_tile)
        self.next_target_tile.create_chiled()

    def run(self):
        while True:
            self.__create_tile()               
            self.__sum_count()
            time.sleep(1)

    def __chk_tile(self):
        # Data Base の関数を使用する。
        pass

    def next_tile(self, tile : Wall.Tile) -> Wall.Tile:
        if isinstance(tile , Wall.TopTile):
            raise ExceptEnd("countOver")
        try:
            n_tile = tile.parent.chiled_tiles[tile.parent.pointer + 1]
            return n_tile
        except IndexError:
            parent_tile = self.next_tile(tile.parent)
            if isinstance(parent_tile , Wall.TopTile):
                raise ExceptEnd("countOver")


    def __create_tile(self):
        if not self.__chk_tile():return
        # 次のtile を作成する。
        #othello 計算を行い、タイルを作成
        parent_tile = self.wall.target_tile.parent
        parent_tile.target_child_finish()
        while True:
            if parent_tile.is_finish:
                parent_tile.parent.taret_child_finish()
                parent_tile = parent_tile.parent
            else :
                break

        (bord, player ) = parent_tile.next_child_bord
        kif_list = ol_count.run_Enumeration(bord,player,level=Wall.LEVEL_THIN)
        tile = self.wall.create_tile(bord, player, kif_list)
        tile.parent = parent_tile
        parent_tile.regist_child(tile)
        self.wall.target_tile = tile
        pass

    def __sum_count(self):
        pass

    def __wall_redy(self):
        pass

def start():
    print("rooter start.")
    root = Root()
    root.redy()
    # thRoot = threading.Thread(target=root.run)
    # thRoot.start()