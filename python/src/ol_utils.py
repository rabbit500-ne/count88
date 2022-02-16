# coding: UTF-8

import dataclasses
from enum import Enum
# import wall
#**************************************************************
# define 
#**************************************************************
HAND_NUM    = 128

BLACK       = 0
WHITE       = 1

INIT_BORD = [0x0000001008000000, 0x0000000810000000]

class PLAYER(Enum):
    black = 0
    white = 1

class BORD(int):pass

@dataclasses.dataclass
class BORD_WB():
    w : BORD = 0
    b : BORD = 0
# BORD[0] : black 
# BORD[1] : white

@dataclasses.dataclass
class Kif():
    bord : BORD_WB = BORD_WB()
    pas : int = 0
    player : PLAYER = 0

    @property
    def name(self):
        return f"{self.bord.b}_{self.bord.w}_{self.pas}_{self.player.value}"

    @name.setter
    def name(self, s : str):
        arr = s.split("_")
        self.bord.b = int(arr[0])
        self.bord.w = int(arr[1])
        self.pas = int(arr[2])
        self.player = PLAYER(int(arr[3]))





#**************************************************************
# Error
#**************************************************************
class ErrorOthelloValue( Exception ):pass


#**************************************************************
# val 
#**************************************************************
def init_bord():
    # [black, white] ?
    return [0x0000001008000000, 0x0000000810000000]

class Othello():
    def __init__(self):
        self.canTble = []
        self.selectedTbl = []
        self.bord = []
        self.moveNum = None
        self.player = None
        self.state = None
        self.start = None
        self.end = None
        pass

# def init_bord( bord ):
#     bord = [[0]*2 for i in range(HAND_NUM)]
#     bord[0] = init_bord()


def bttoh( bord):
    ret = 0
    for i in range(0,8):
        if(0x0101010101010101 << i) & bord:
            ret = i+1
            break
    for i in range(0, 8):
        if((0x00000000000000FF) << (i * 8)) & bord:
            ret = ret | ((i+1) * 0x10)
            break
    return ret

def debug_preview_bord( bord, hand, selected):
    i = 0;
    print( "W:0x%016x" % bord[WHITE])
    print( "B:0x%016x" % bord[BLACK])

def search(bord : BORD_WB, hand):
    can = 0
    b_bord = bord.b
    w_bord = bord.w
    p = b_bord if hand == PLAYER.black else w_bord
    o = w_bord if hand == PLAYER.black else b_bord
    shift = [1, 7, 8, 9]
    masks = [0x7e7e7e7e7e7e7e7e, 
            0x007e7e7e7e7e7e00, 
            0x00FFFFFFFFFFFF00, 
            0x007e7e7e7e7e7e00]
    blank = ~(p | o)
    for i in range(4):
        o2 = masks[i] & o;
        t = o2 & (p << shift[i]);           #黒石の左隣にある白石を調べる	
        t |= o2 & (t << shift[i]);                  #その隣の
        t |= o2 & (t << shift[i]);                  #隣の・・・
        t |= o2 & (t << shift[i]);
        t |= o2 & (t << shift[i]);
        t |= o2 & (t << shift[i]);			#一度にひっくり返せる石は6つまで
        can |= blank & (t << shift[i]);    #着手出来るのは空白のマスだけ
    for i in range(4):
        o2 = masks[i] & o;
        t = o2 & (p >> shift[i]);           #黒石の左隣にある白石を調べる	
        t |= o2 & (t >> shift[i]);                  #その隣の
        t |= o2 & (t >> shift[i]);                  #隣の・・・
        t |= o2 & (t >> shift[i]);
        t |= o2 & (t >> shift[i]);
        t |= o2 & (t >> shift[i]);			#一度にひっくり返せる石は6つまで
        can |= blank & (t >> shift[i]);    #着手出来るのは空白のマスだけ
    return can

def ConvStrBordToHex( bord):
    """
    00000000
    00000000
    00000000
    00010000   -->  0x0000001008000000
    00001000
    00000000
    00000000
    00000000
    """
    val = 0
    
    for s in bord:
        if s in ['\n', ' ']:
            continue
        try:
            val = val + int(s)
            val = val << 1
        except Exception as e:
            print(e)
            print(s)
    return val >> 1

def ConvStrBordToHexWB( bord):
    """
    00000000
    00000000
    00000000
    000bw000   -->  [0x0000001008000000,
    000wb000           0x0000000810000000]
    00000000
    00000000
    00000000
    """
    w = 0
    b = 0
    for s in bord:
        if s in ['\n', ' ']:
            continue
        try:
            if s == 'b':
                b = b + 1
            if s == 'w':
                w = w + 1
            w = w << 1
            b = b << 1
        except Exception as e:
            print(e)
            print(s)
    return [b >> 1, w >> 1]

def print_bord(bord):
    s = "\n"
    for i in range(64):
        s = ("1" if 1 & bord else "0") + s
        if i % 8 == 7 :
            s = '\n' + s
        bord >>= 1
    print(s)

def print_bordWB(bord):
    b = bord[0]
    w = bord[1]
    s = "\n"

    for i in range(64):
        if 1 & b :
            s = "b" + s
        elif 1 & w :
            s = "w" + s
        else :
            s = "0" + s
        if i % 8 == 7:
            s = '\n' + s
        b >>= 1
        w >>= 1
    
    print(s)
    


        
def select_hand(can,selected):
    """
    """
    if can & selected != selected:
        print("can")
        print_bord(can)
        print("selected")
        print_bord(selected)
        raise ErrorOthelloValue()
    val = can ^ selected
    return val & -val


def reverse(bord, selected, player):
    o = bord.b if player == PLAYER.white else bord.w
    p = bord.w if player == PLAYER.white else bord.b
    pos = 63 - clz(selected)
    flipped = 0

    x = o
    yzw = o & 0x7e7e7e7e7e7e7e7e

    mask = 0x0080808080808080 >> (63 - pos)
    outflank = (0x8000000000000000 >> clz(~x & mask)) & p
    flipped |= (-outflank * 2) & mask

    mask = 0x7f00000000000000 >> (63 - pos)
    outflank = (0x8000000000000000 >> clz(~yzw & mask)) & p
    flipped |= (-outflank * 2) & mask

    mask = 0x0102040810204000 >> (63 - pos)
    outflank = (0x8000000000000000 >> clz(~yzw & mask)) & p
    flipped |= (-outflank * 2) & mask

    mask = 0x0040201008040201 >> (63 - pos)
    outflank = (0x8000000000000000 >> clz(~yzw & mask)) & p
    flipped |= (-outflank * 2) & mask

    mask = 0x0101010101010100 << pos
    outflank = mask & ((x | ~mask) + 1) & p
    flipped |= (outflank - (outflank != 0)) & mask

    mask = 0x00000000000000fe << pos
    outflank = mask & ((yzw | ~mask) + 1) & p
    flipped |= (outflank - (outflank != 0)) & mask

    mask = 0x0002040810204080 << pos
    outflank = mask & ((yzw | ~mask) + 1) & p
    flipped |= (outflank - (outflank != 0)) & mask

    mask = 0x8040201008040200 << pos
    outflank = mask & ((yzw | ~mask) + 1) & p
    flipped |= (outflank - (outflank != 0)) & mask

    o &= ~flipped
    p |= flipped
    p |= (1 << (63 - clz(selected)))

    if player == PLAYER.black :
        return BORD_WB(b=p,w=o)
            # [p,o]
    else :
        return BORD_WB(b=o, w=p)
        # [o, p]
    
def player_change(player):
    if player == PLAYER.black:
        return PLAYER.white
    if player == PLAYER.white:
        return PLAYER.black
    raise Exception("player ERR")

def clz(  n):
    for i in range(64):
        if( n & 0x8000000000000000):
            return i;
        n <<= 1;
    return 0










if __name__ == "__main__":
    o = Othello()
    o.init_bord()
    print(o.bord[0])
    o.debug_preview_bord( o.bord[0], 1,1)
