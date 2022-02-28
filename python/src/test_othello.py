import unittest
import ol_utils as util
import ol_count as cot
# import parameterized

class TestUnit_ol_utils(unittest.TestCase):
    def test_init(self):
        o = util.Othello()
        util.init_bord()

    def test_ConvStrBordToHex(self):
        bord = \
        """
        00000000
        00000000
        00000000
        00010000
        00001000
        00000000
        00000000
        00000000
        """
        b = util.ConvStrBordToHex(bord)
        self.assertEqual(bin(b),bin(0x0000001008000000))

    def test_search(self):
        correct = \
            """
            00000000
            00000000
            00001000
            00000100
            00100000
            00010000
            00000000
            00000000
            """
        correct_bord= util.ConvStrBordToHex(correct)
        bord=util.BORD_WB(
            b=util.INIT_BORD[0],
            w=util.INIT_BORD[1]
        )
        bord = util.search(bord, util.PLAYER.black)
        self.assertEqual(bord,correct_bord)

    def test_search_2(self):
        bord = \
            """
            00000000
            00000000
            00000000
            000bw000
            000wbb00
            00b00000
            00000bw0
            0000000w            
            """
        correct_b = \
            """
            00000000
            00000000
            00011100
            00000100
            00100000
            00010000
            00000001
            00000000
            """
        [b, w] = util.ConvStrBordToHexWB(bord)
        bord = util.BORD_WB(b=b,w=w)
        ret = util.search(bord,util.PLAYER.black)
        self.assertEqual(ret,util.ConvStrBordToHex(correct_b))

    def test_select_hand(self):
        _can = \
            """
            00000000
            00000000
            00011100
            00000100
            00100000
            00010000
            00000001
            00000000
            """
        _selected = \
            """
            00000000
            00000000
            00000000
            00000000
            00000000
            00010000
            00000001
            00000000
            """
        _correct = \
            """
            00000000
            00000000
            00000000
            00000000
            00100000
            00000000
            00000000
            00000000
            """
        can = util.ConvStrBordToHex(_can)
        selected = util.ConvStrBordToHex(_selected)
        correct = util.ConvStrBordToHex(_correct)
        self.assertEqual(correct, util.select_hand(can, selected))

    def test_select_hand_error(self):
        _can = \
            """
            00000000
            00000000
            00011100
            00000100
            00100000
            00010000
            00000001
            00000000
            """
        _selected = \
            """
            00000000
            00000000
            00000000
            00000000
            00000000
            00011000
            00000001
            00000000
            """

        can = util.ConvStrBordToHex(_can)
        selected = util.ConvStrBordToHex(_selected)

        with self.assertRaises(util.ErrorOthelloValue):
            util.select_hand(can, selected)

    def test_reverse(self):
        _bord = \
            """
            00000000
            00000000
            00000000
            000bw000
            000wbb00
            00b00000
            00000bw0
            0000000w            
            """
        _selected = \
            """
            00000000
            00000000
            00000000
            00000000
            00100000
            00000000
            00000000
            00000000            
            """
        _correct_bord = \
            """
            00000000
            00000000
            00000000
            000bw000
            00bbbb00
            00b00000
            00000bw0
            0000000w            
            """
        [b, w] = util.ConvStrBordToHexWB(_bord)
        selected = util.ConvStrBordToHex(_selected)
        [cb,cw] = util.ConvStrBordToHexWB(_correct_bord)
        bord = util.BORD_WB(b=b,w=w)
        ret_bord = util.reverse(bord, selected, util.PLAYER.black)

        # util.print_bord(ret_bord[0])
        # util.print_bord(ret_bord[1])
        # util.print_bordWB(correct_bord)
        correct_bord = util.BORD_WB(b=cb,w=cw)
        self.assertEqual(ret_bord,correct_bord)


class Testunit_ol_count( unittest.TestCase ):
    def test_run_return(self):
        _bord = \
            """
            0wbwbwww
            bbwwbwbw
            bbbbwwww
            bbwwwbbb
            bbwwbwbw
            bwbwwwbw
            bwbwbwwb
            bwbwwbbb            
            """
        [b, w] = util.ConvStrBordToHexWB(_bord)
        bord = util.BORD_WB(b=b,w=w)
        count = cot.run_return(bord, util.PLAYER.black)
        self.assertEqual(count, 1)
        print("-------------")

    def test_run_return_02(self):
        _bord = \
            """
            00bwbwww
            wbwwbwbw
            bbbbwwww
            bbwwwbbb
            wbwwbwbw
            bwbwwwbw
            bwbwbwwb
            bwbwwbbb            
            """
        [b, w] = util.ConvStrBordToHexWB(_bord)
        bord = util.BORD_WB(b=b,w=w)
        count = cot.run_return(bord, util.PLAYER.black)
        self.assertEqual(count, 2)

    def test_run_return_03(self):
        _bord = \
            """
            000wbwww
            wbwwbwbw
            bbbbwwww
            bbwwwbbb
            wbwwbwbw
            bwbwwwbw
            bwbwbwwb
            bwbwwbbb            
            """
        [b, w] = util.ConvStrBordToHexWB(_bord)
        bord = util.BORD_WB(b=b,w=w)
        count = cot.run_return(bord, util.PLAYER.black)
        self.assertEqual(count, 5)

    def test_run_Enumeration(self):
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
        [b, w] = util.ConvStrBordToHexWB(_bord)
        kif = util.Kif(
            bord=util.BORD_WB(b=b,w=w),
            pas=0,
            player=util.PLAYER.black,
        )
        bord_list = cot.run_Enumeration(kif, 2)
        self.assertEqual(len(bord_list), 12)





if __name__ == "__main__":
    unittest.main()

    