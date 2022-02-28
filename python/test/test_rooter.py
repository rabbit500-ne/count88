import pytest
import sys

sys.path.append("../src")
import rooter

def test_redy():
    root = rooter.Root()
    root.redy()
