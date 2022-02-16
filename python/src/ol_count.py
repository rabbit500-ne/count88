# coding: UTF-8
import ol_utils as util 
import threading 
import time
from typing import List

from ol_utils import BORD_WB

def run_count(count):
    """
    return : kifu
    """
    pass

def run_return(bord : util.BORD_WB, player):
    """
    return : count
    """
    can = [0 for x in range(125)]
    selected = [0 for  x  in range(125)]
    bords = [None for x in range(125)]
    bords[0] = bord
    status = 1
    stage = 0
    select = 0
    pass_count = 0
    count = 0
    while(True):
        if status == 1:
            can[stage] = util.search(bords[stage], player)
            selected[stage] = 0
            util.print_bord(can[stage])
            if can[stage] == 0:
                select = 0
                pass_count += 1
                if pass_count == 2:
                    pass_count = 0
                    count += 1
                    stage -= 2
                    status = 3
                    print("1->3 {0}".format(stage))
                else :
                    bords[stage + 1] = bords[stage]
                    stage += 1
                    player = util.player_change(player)
                    print("1->1 {0}".format(stage))
            else :
                select = util.select_hand(can[stage], selected[stage])
                pass_count = 0
                status = 2
                print("1->2 {0}".format(stage))
        elif status == 2:
            bords[stage + 1] = util.reverse(bords[stage], select, player)
            selected[stage] |= select
            stage += 1
            player = util.player_change(player)
            status = 1
            print("2->1 {0}".format(stage))

        elif status == 3:
            select = util.select_hand(can[stage], selected[stage])
            if select == 0:
                stage -= 1
                player = util.player_change(player)
                print("3->3 {0}".format(stage))
                if stage < 0:
                    return count
            else :
                status = 2
                print("3->2 {0}".format(stage))


def run_Enumeration(kif : util.Kif, level):
    """
    return kifu Array
    """
    can = [0 for x in range(125)]
    selected = [0 for  x  in range(125)]
    bords : List[BORD_WB]= [None for x in range(125)]
    bords[0] = kif.bord
    player = kif.player
    status = 1
    stage = 0
    select = 0
    pass_count = kif.pas
    count = 0
    kifu_list : List[util.Kif] = []
    while(True):
        if status == 1:
            util.print_bordWB([bords[stage].b,bords[stage].w])
            can[stage] = util.search(bords[stage], player)
            selected[stage] = 0
            util.print_bord(selected[stage])
            util.print_bord(can[stage])
            if can[stage] == 0:
                select = 0
                pass_count += 1
                if pass_count == 2:
                    count += 1
                    kif = util.Kif(
                        bord = bords[stage],
                        pas = pass_count,
                        player = player)
                    kifu_list.append(kif)
                    stage -= 2
                    pass_count = 0
                    if stage <= 0:
                        # kifu_list.append(util.Kif(
                        #     bord=bords[stage + 1],
                        #     pas=pass_count,
                        #     player=player))
                        return kifu_list
                    status = 3
                    print("1->3 {0}".format(stage ))
                elif pass_count > 2: #debug
                    raise Exception  #debug
                else :
                    bords[stage + 1] = bords[stage]
                    stage += 1
                    player = util.player_change(player)
                    print(f"1->1 :{stage} :pas{pass_count}")
            else :
                select = util.select_hand(can[stage], selected[stage])
                pass_count = 0
                status = 2
                print(f"1->2 :{stage} :pas{pass_count}")
        elif status == 2:
            util.print_bordWB([bords[stage].b,bords[stage].w])
            util.print_bord(selected[stage])
            bords[stage + 1] = util.reverse(bords[stage], select, player)
            selected[stage] |= select
            if stage + 1 >= level:
                kifu_list.append(util.Kif(
                    bord=bords[stage + 1],
                    pas=pass_count,
                    player=player))
                status = 3
                print(f"2->3 :{stage}: pass{pass_count}")
            else :    
                stage += 1
                player = util.player_change(player)
                status = 1
                print("2->1 {0}".format(stage))

        elif status == 3:
            util.print_bordWB([bords[stage].b,bords[stage].w])
            util.print_bord(selected[stage])
            try:
                select = util.select_hand(can[stage], selected[stage])
            except:
                print(f"{pass_count}")
                print("bors[stage]")
                raise Exception
            if select == 0:
                stage -= 1
                player = util.player_change(player)
                print(f"3->3 :{stage}: pass{pass_count}")
                if stage < 0:
                    return kifu_list
            else :
                status = 2
                print("3->2 {0}".format(stage))
