import unittest
import sys
sys.path.append("../")
import othello_count
import wall2 as WALL

class modTest_othello_main(unittest.TestCase):
    def test_main(self):
        othello_count.main()

class modTest_client(unittest.TestCase):
    def test_test(self):
        pass

class modTest_kifuDB( unittest.TestCase):
    def test_migrate(self):
        kifuDB = WALL.kifuDB()
        kifuDB.migrate()
        