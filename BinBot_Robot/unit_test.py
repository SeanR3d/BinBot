import os
import sys
import unittest


def main():

    suite = unittest.TestLoader().discover('./test')

    test_suite = unittest.TestSuite(suite)
    text_runner = unittest.TextTestRunner(verbosity=2).run(test_suite)

    pass


if __name__ == '__main__':
    main()
