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
        duplicates = False
        for word in check_list:
            leet_word = word
            for old, new in leet_replacements:
                leet_word = leet_word.replace(old, new)
            if line.lower().count(word) > 1:
                duplicates = True
            leet_line = line.lower()
            for old, new in leet_replacements:
                leet_line = leet_line.replace(old, new)
            if leet_line.count(leet_word) > 1:
                duplicates = True
        if duplicates is False:
            print(line)


leet_replacements = (
    ('o', '0'), ('a', '4'), ('a', '@'), ('b', '6'), ('e', '3'), ('g', '9'), ('i', '1'), ('i', '!'),
    ('l', '1'), ('s', '5'), ('s', '$'), ('t', '7'))

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
        # input_list.add(word.capitalize().swapcase())
        # Leet text
        leet_word = word
        for old, new in leet_replacements:
            leet_word = leet_word.replace(old, new)
        check_list.add(leet_word)
        input_list.add(leet_word)
        input_list.add(leet_word.capitalize())
        input_list.add(leet_word.swapcase())

iterators = [itertools.permutations(input_list, 2),
             itertools.permutations(input_list, 3),
             itertools.permutations(input_list, 4),
             itertools.permutations(input_list, 5)]

jobs = []
for iterator in iterators:
    with multiprocessing.Pool() as pool:
        pool.map(printer, iterator)
