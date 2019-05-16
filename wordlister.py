import itertools
import sys
import multiprocessing

if len(sys.argv) < 4:
    print('Missing arguments:\n\t{} [input_file] [min-length] [max-length]'.format(sys.argv[0]))
    sys.exit()


def printer(combo):
    line = ''.join(combo)
    length = len(line)
    if length == 0:
        return False
    elif int(sys.argv[2]) <= length <= int(sys.argv[3]):
        for word_check in check_list:
            if line.lower().count(word_check) > 1:
                return True
        print(line)
        # Leet
        for old, new in leet_replacements:
            line = line.replace(old, new)
        print(line)
    return True


leet_replacements = (
    ('o', '0'), ('O', '0'), ('a', '4'), ('A', '4'), ('e', '3'), ('E', '3'), ('i', '1'), ('I', '1'), ('s', '5'),
    ('S', '5'))

input_list = set()
check_list = set()

with open(sys.argv[1], 'r') as input_file:
    for row in input_file:
        word = row.rstrip('\n')
        check_list.add(word)
        input_list.add(word)
        input_list.add(word.capitalize())
        input_list.add(word.swapcase())

iterators = set()
n_perm = 5
for x in range(n_perm):
    x += 1
    iterators.add(itertools.permutations(input_list, x))

slices = set()
step = 1000000
for iterator in iterators:
    start = 0
    stop = start + step
    next_it = False
    while 1:
        if next_it is False:
            cake_slice = itertools.islice(iterator, start, stop)
        else:
            cake_slice = itertools.islice(iterator, start, None)
        with multiprocessing.Pool() as pool:
            data = pool.map(printer, cake_slice)
        start += step
        stop += step
        if next_it is True:
            break
        if len(data) == 0:
            next_it = True
