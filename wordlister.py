import itertools
from multiprocessing import Pool
import argparse

parser = argparse.ArgumentParser(description='A simple wordlist generator and mangler written in python.')
required = parser.add_argument_group('required arguments')
# Required arguments
required.add_argument('--input', help='Input file name', required=True)
required.add_argument('--perm', help='Max number of words to be combined on the same line', required=True)
required.add_argument('--min', help='Minimum generated password length', required=True)
required.add_argument('--max', help='Maximum generated password length', required=True)
# Optional arguments
parser.add_argument('--test', help='Output first N iterations (single process/core)', required=False)
parser.add_argument('--cores', help='Manually specify processes/cores pool that you want to use', required=False)
parser.add_argument('--leet', help='Activate l33t mutagen', action='store_true')
parser.add_argument('--cap', help='Activate capitalize mutagen', action='store_true')
parser.add_argument('--up', help='Activate uppercase mutagen', action='store_true')
parser.add_argument('--append', help='Append chosen word (append \'word\' to all passwords)', required=False)
parser.add_argument('--prepend', help='Append chosen word (prepend \'word\' to all passwords)', required=False)

args = parser.parse_args()


def worker(combo_worker):
    line_worker = ''.join(combo_worker)
    printer(check_list, line_worker)
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
        if args.cores is None:
            with Pool() as pool:
                data = pool.map(worker, cake_slice)
        else:
            with Pool(int(args.cores)) as pool:
                data = pool.map(worker, cake_slice)
        start += step
        stop += step
        if next_it is True:
            break
        if len(data) == 0:
            next_it = True


def repetition_check(line_repetition: str, check_list_repetition):
    for word_check in check_list_repetition:
        if line_repetition.lower().count(word_check) > 1:
            return True
    return False


def leet(check_list_leet,leet_replacements_leet, line_leet, out_counter_leet, trigger_counter_leet=False):
    line_leet_old = line_leet
    for old_leet, new_leet in leet_replacements_leet:
        line_leet = line_leet.replace(old_leet, new_leet)
    if line_leet != line_leet_old:
        out_counter_leet = printer(check_list_leet, line_leet, out_counter_leet, trigger_counter_leet)
    return out_counter_leet


def test(check_list_test, x_test, out_counter_test):
    for combo in itertools.permutations(input_list, x_test + 1):
        line = ''.join(combo)
        out_counter_test += printer(check_list_test, line, out_counter_test, True)
        if out_counter_test >= int(args.test):
            return out_counter_test
    return out_counter_test


def printer(check_list_printer, line_printer, out_counter=0, trigger_counter=False, leet_trigger=True):
    length_worker = len(line_printer)
    if length_worker == 0:
        return out_counter
    elif int(args.min) <= length_worker <= int(args.max):
        if repetition_check(line_printer, check_list_printer) is True:
            return out_counter
        print(line_printer)
        if trigger_counter is True:
            out_counter += 1
            if out_counter >= int(args.test):
                return out_counter
        if args.append is not None:
            print(line_printer + args.append)
            if trigger_counter is True:
                out_counter += 1
                if out_counter >= int(args.test):
                    return out_counter
        if args.prepend is not None:
            print(args.prepend + line_printer)
            if trigger_counter is True:
                out_counter += 1
                if out_counter >= int(args.test):
                    return out_counter
        if args.leet is True and leet_trigger is True:
            if trigger_counter is False:
                out_counter += leet(check_list_printer, leet_replacements, line_printer, out_counter)
            else:
                out_counter += leet(check_list_printer, leet_replacements, line_printer, out_counter, True)
    return out_counter


leet_replacements = (
    ('o', '0'), ('O', '0'), ('a', '4'), ('A', '4'), ('e', '3'), ('E', '3'), ('i', '1'), ('I', '1'), ('s', '5'),
    ('S', '5'))

input_list = set()
check_list = set()

with open(args.input, 'r') as input_file:
    for row in input_file:
        word = row.rstrip('\n')
        check_list.add(word)
        input_list.add(word)
        if args.cap is True:
            input_list.add(word.capitalize())
        if args.up is True:
            input_list.add(word.upper())

if args.test is not None:
    counter = 0
    for x in range(int(args.perm)):
        counter = test(check_list, x, counter)
        if counter >= int(args.test):
            break
else:
    for x in range(int(args.perm)):
        slice_and_run(itertools.permutations(input_list, x + 1))
