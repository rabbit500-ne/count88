
#------------------------------------------------
# 統計管理
#------------------------------------------------
# class Db 依存

import threading
import wall2 as Wall
import time
import ol_count

class Root():
    def __init__(self):
        self.wall = Wall.Wall()
        pass

    def redy(self):
        # DB にアクセス
        self.wall.redy()
        # 注視するテーブルを決める
        # DBが完成していなかったら作成する。

        pass

    def run(self):
        while True:
            self.__create_tile()               
            self.__sum_count()
            time.sleep(1)

    def __chk_tile(self) -> bool:
        # Data Base の関数を使用する。
        return True

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