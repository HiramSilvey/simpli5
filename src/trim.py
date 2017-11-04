"""
Take in a list of words from INPUT_FILE and write a list of the word stems the OUTPUT_FILE.
Usage:
    trim.py INPUT_FILE OUTPUT_FILE
"""

from stemming.porter2 import stem
from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)
    print(args)
