from stemming.porter2 import stem

def _parse_trim(PATH_FILE, DIR_FILE):
    lib = []
    for line in open(PATH_FILE):
        line = line.rstrip('\n')
        lib.append(stem(line))

    f = open(DIR_FILE, 'w')
    for i in range(len(lib)):
        f.write(lib[i] + '\n')

    f.close()

_parse_trim("../data/google-10000-english-usa.txt", "../data/trim.txt")

