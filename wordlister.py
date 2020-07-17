#!/usr/bin/python3
"""Wordlister, a simple wordlist generator and mangler written in python 3.8."""
# Written By Ananke: https://github.com/4n4nk3

import argparse
from itertools import islice, permutations
from multiprocessing import Pool
from os import remove
from sys import exit
from typing import Iterator, List

TEMP_OUTPUT_FILE = 'temp-output.txt'
OUTPUT_FILE = 'output.txt'
LEET_TRANSLATIONS = str.maketrans('oOaAeEiIsS', '0044331155')


def init_argparse() -> argparse.ArgumentParser:
    """
    Define and manage arguments passed to Wordlister via terminal.

    :return argparse.ArgumentParser
    """

    parser = argparse.ArgumentParser(
        description='A simple wordlist generator and mangler written in python.')
    required = parser.add_argument_group('required arguments')
    # Required arguments
    required.add_argument('--input', help='Input file name', required=True)
    required.add_argument('--perm', help='Max number of words to be combined on the same line',
                          required=True, type=int)
    required.add_argument('--min', help='Minimum generated password length', required=True,
                          type=int)
    required.add_argument('--max', help='Maximum generated password length', required=True,
                          type=int)
    # Optional arguments
    parser.add_argument('--test', help='Output first N iterations (single process/core)',
                        required=False, type=int)
    parser.add_argument('--cores',
                        help='Manually specify processes/cores pool that you want to use',
                        required=False, type=int)
    parser.add_argument('--leet', help='Activate l33t mutagen', action='store_true')
    parser.add_argument('--cap', help='Activate capitalize mutagen', action='store_true')
    parser.add_argument('--up', help='Activate uppercase mutagen', action='store_true')
    parser.add_argument('--append', help='Append chosen word (append \'word\' to all passwords)',
                        required=False)
    parser.add_argument('--prepend', help='Prepend chosen word (prepend \'word\' to all passwords)',
                        required=False)
    return parser


def printer(combo_printer: List) -> set:
    """
    Print generated words to stdout and in case apply chosen mutagens (append, prepend, leet).

    :param combo_printer: a slice of the word list that must be elaborated
    :type combo_printer: List
    :return data: set
    """
    data = set()
    if len(set(map(str.lower, combo_printer))) == len(combo_printer):
        line_printer = ''.join(combo_printer)
        if args.min <= len(line_printer) <= args.max:
            data.add(line_printer)
            if args.append is not None and len(line_printer) + len(args.append) <= args.max:
                data.add(f'{line_printer}{args.append}')
            if args.prepend is not None and len(line_printer) + len(args.prepend) <= args.max:
                data.add(f'{args.prepend}{line_printer}')
            if args.leet is True:
                for x in leet(line_printer):
                    data.add(x)
    if data:
        return data


def slice_and_run(single_iterator: Iterator):
    """
    Makes slices from iterator and process them via a process pool.

    :param single_iterator: Iterator returning permutations to be sliced and sent to printer() func
    :type single_iterator: Iterator
    """
    step = 10000000
    start = 0
    check = True
    with open(TEMP_OUTPUT_FILE, 'a') as out_f:
        with Pool(args.cores) as pool:
            while check:
                check = False
                cake_slice = islice(single_iterator, start, start + step)
                data = (result for result in pool.map(printer, cake_slice) if result)
                for result in data:
                    check = True
                    out_f.write('\n'.join(result) + '\n')
                start += step


def leet(line_leet: str) -> str:
    """
    Generator that returns the leeted version of a string and also returns it with applied prepend
    and append mutagens if required by user's parameters.

    :param line_leet: the string to be leeted
    :type line_leet: str
    :return _: str
    """

    line_leet = line_leet.translate(LEET_TRANSLATIONS)
    yield line_leet
    if args.append is not None:
        yield f'{line_leet}{args.append}'
    if args.prepend is not None:
        yield f'{args.prepend}{line_leet}'


def test_printer(x_test: int, out_counter_test: int) -> int:
    """Test printer."""
    input_list = read_input_file(args.input)
    for combo in permutations(input_list, x_test + 1):
        if len(set(map(str.lower, combo))) == len(combo):
            line = ''.join(combo)
            if args.min <= len(line) <= args.max:
                print(line)
                out_counter_test += 1
                if out_counter_test >= args.test:
                    return out_counter_test
                if args.append is not None:
                    print(f'{line}{args.append}')
                    out_counter_test += 1
                    if out_counter_test >= args.test:
                        return out_counter_test
                if args.prepend is not None:
                    print(f'{args.prepend}{line}')
                    out_counter_test += 1
                    if out_counter_test >= args.test:
                        return out_counter_test
                if args.leet is True:
                    line = line.translate(LEET_TRANSLATIONS)
                    print(line)
                    out_counter_test += 1
                    if out_counter_test >= args.test:
                        return out_counter_test
                    if args.append is not None:
                        print(f'{line}{args.append}')
                        out_counter_test += 1
                        if out_counter_test >= args.test:
                            return out_counter_test
                    if args.prepend is not None:
                        print(f'{args.prepend}{line}')
                        out_counter_test += 1
                        if out_counter_test >= args.test:
                            return out_counter_test
    return out_counter_test


def read_input_file(file_path: str) -> set:
    """
    Read input file and return a set of words.

    :param file_path: the path to the file with the user supplied wordlist
    :type file_path: str
    :return _: set
    """

    try:
        with open(file_path, 'r') as input_file:
            data = input_file.read().splitlines()
    except FileNotFoundError:
        print('Input file not found!\nExiting...')
        exit(1)
    # Apply capitalize mutagen and upper mutagen if needed
    input_list = set(data)
    for word in data:
        if args.cap is True:
            input_list.add(word.capitalize())
        if args.up is True:
            input_list.add(word.upper())
    return input_list


def test_run():
    """Test run to generate only N words."""

    out_counter = 0
    n_perm = args.perm
    n_test = args.test
    for x in range(n_perm):
        out_counter = test_printer(x, out_counter)
        if out_counter >= n_test:
            break


def real_run() -> None:
    """Real run."""

    input_list = read_input_file(args.input)
    n_perm = args.perm
    for x in range(n_perm):
        my_iterator = permutations(input_list, x + 1)
        slice_and_run(my_iterator)


args = init_argparse().parse_args()

if __name__ == '__main__':
    # Test run or real run
    if args.test is not None:
        test_run()
    else:
        open(OUTPUT_FILE, 'w').write('')
        open(TEMP_OUTPUT_FILE, 'w').write('')
        real_run()
        definitive = set()
        with open(TEMP_OUTPUT_FILE, 'r') as f_in:
            with open(OUTPUT_FILE, 'a') as f_out:
                for my_line in f_in:
                    if my_line not in definitive:
                        definitive.add(my_line)
                        f_out.write(my_line)
        remove(TEMP_OUTPUT_FILE)
        print('\nOutput saved to \'output.txt\'!\n')
