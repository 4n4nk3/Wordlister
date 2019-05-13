import itertools
import sys
import multiprocessing

global check_list
global min_length
global max_length
global leet_replacements

if len(sys.argv) < 4:
    print('Missing arguments:\n\t{} [input_file] [min-lenght] [max-lenght]'.format(sys.argv[0]))
    sys.exit()

min_length = int(sys.argv[2])
max_length = int(sys.argv[3])


def printer(combo):
    line: str = ''.join(combo)
    length = len(line)
    if length >= min_length and length <= max_length:
        for word in check_list:
            if line.lower().count(word) > 1:
                return False
        print(line)
        # Leet
        for old, new in leet_replacements:
            line = line.replace(old, new)
        print(line)
        return True


leet_replacements = (
    ('o', '0'), ('O', '0'), ('a', '4'), ('A', '4'), ('e', '3'), ('E', '3'), ('g', '9'), ('G', '9'), ('i', '1'),
    ('I', '1'), ('l', '1'), ('L', '1'), ('s', '5'), ('S', '5'), ('t', '7'), ('T', '7'))

input_list = set()
check_list = set()

with open(sys.argv[1], 'r') as input_file:
    for row in input_file:
        word = row[:-1]
        # Plain text
        check_list.add(word)
        input_list.add(word)
        input_list.add(word.capitalize())
        input_list.add(word.swapcase())

jobs = []
n_perm = 5
for x in range(n_perm):
    x += 1
    with multiprocessing.Pool() as pool:
        pool.map(printer, itertools.permutations(input_list, x))
