import itertools
from sys import argv, exit
from multiprocessing import Pool

if len(argv) < 4:
    print('Missing arguments:\n\t{} [input_file] [min-length] [max-length] [n-combinations]'.format(argv[0]))
    exit()


def printer(combo):
    line = ''.join(combo)
    length = len(line)
    if length == 0:
        return False
    elif int(argv[2]) <= length <= int(argv[3]):
        for word_check in check_list:
            if line.lower().count(word_check) > 1:
                return True
        print(line)
        # Leet
        for old, new in leet_replacements:
            line = line.replace(old, new)
        print(line)
    return True


def slice_and_run(single_iterator):
    step = 10000000
    start = 0
    stop = start + step
    next_it = False
    while 1:
        if next_it is False:
            cake_slice = itertools.islice(single_iterator, start, stop)
        else:
            cake_slice = itertools.islice(single_iterator, start, None)
        with Pool() as pool:
            data = pool.map(printer, cake_slice)
        start += step
        stop += step
        if next_it is True:
            break
        if len(data) == 0:
            next_it = True


leet_replacements = (
    ('o', '0'), ('O', '0'), ('a', '4'), ('A', '4'), ('e', '3'), ('E', '3'), ('i', '1'), ('I', '1'), ('s', '5'),
    ('S', '5'))

input_list = set()
check_list = set()

with open(argv[1], 'r') as input_file:
    for row in input_file:
        word = row.rstrip('\n')
        check_list.add(word)
        input_list.add(word)
        input_list.add(word.capitalize())
        input_list.add(word.swapcase())

for x in range(int(argv[4])):
    slice_and_run(itertools.permutations(input_list, x+1))
