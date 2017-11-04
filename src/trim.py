"""
Take in a list of words from INPUT_FILE and write a list of the word stems the OUTPUT_FILE.
Usage:
    trim.py INPUT_FILE OUTPUT_FILE
"""

from stemming.porter2 import stem
from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)
    lib = []
    for line in open(args['INPUT_FILE']):
        line = line.rstrip('\n')
        lib.append(stem(line))

    f = open(args['OUTPUT_FILE'], 'w')
    for i in range(len(lib)):
        f.write(lib[i] + '\n')

    f.close()
