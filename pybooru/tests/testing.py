import unittest2
import os


def main():
    # Change dir to current dir to make sure unittest2 only discoveres tests
    # in the pybooru/tests/ dir.
    os.chdir(os.path.dirname(__file__))
    unittest2.main(None)
