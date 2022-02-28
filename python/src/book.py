import wall2 as wall
import time
import sys

def hook(type, value, tb):
   if hasattr(sys, 'ps1') or not sys.stderr.isatty():
      sys.__excepthook__(type, value, tb)
   else:
      import traceback, pdb
      traceback.print_exception(type, value, tb)
      print()
      pdb.pm()

sys.excepthook = hook


def print_proc_time(f):
    """ 計測デコレータ """
    def print_proc_time_func(*args, **kwargs):
        # 開始
        start_time = time.process_time()
        # 関数実行
        return_val = f(*args, **kwargs)
        # 修了
        end_time = time.process_time()
        # 関数名と経過時間を出力(秒)
        elapsed_time = end_time - start_time
        print(f.__name__, elapsed_time)
        # 戻り値を返す
        return return_val 
    return print_proc_time_func


@print_proc_time
def wall_seader():
    ws = wall.wall_sheeder()
    ws.start()

@print_proc_time
def wall_sheeder_one():
    ws = wall.wall_sheeder()
    ws.create_wood()
    ws.sheeder_tile_LEVEL_0()
    ws.sheeder_tile_LEVEL_X

@print_proc_time
def wall_reader():
    wr = wall.wall_reader()
    wr.read()

def dbclient():
    db = wall.dbi()
    
    def select(column, table_name, if_column, if_value):
        cmd = f"SELECT * FROM {table_name}"
        db.cur.execute(cmd)
        lst = db.cur.fetchone()
        return lst

    l = select()

    




if __name__ == "__main__":
    wall_reader()