# coding: UTF-8
import ol_utils as util
import threading 
import time

def run_count(count):
    """
    return : kifu
    """
    pass

def run_return(bord, player):
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
                selected[stage] = 0
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


def run_Enumeration(bord, player, level):
    """
    return kifu Array
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
    kifu_list = []
    while(True):
        if status == 1:
            can[stage] = util.search(bords[stage], player)

            util.print_bord(can[stage])
            if can[stage] == 0:
                select = 0
                pass_count += 1
                if pass_count == 2:
                    pass_count = 0
                    count += 1
                    kifu_list.append([bords[stage],pass_count,player])
                    stage -= 2
                    status = 3
                    print("1->3 {0}".format(stage))
                else :
                    bords[stage + 1] = bords[stage]
                    stage += 1
                    player = util.player_change(player)
                    print("1->1 {0}".format(stage))
            else :
                selected[stage] = 0
                select = util.select_hand(can[stage], selected[stage])
                pass_count = 0
                status = 2
                print("1->2 {0}".format(stage))
        elif status == 2:
            bords[stage + 1] = util.reverse(bords[stage], select, player)
            selected[stage] |= select
            if stage + 1 >= level:
                kifu_list.append([bords[stage + 1],pass_count,player])
                status = 3
                print("2->3 {0}".format(stage))
            else :    
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
                    return kifu_list
            else :
                status = 2
                print("3->2 {0}".format(stage))
