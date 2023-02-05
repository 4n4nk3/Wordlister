#!/usr/bin/python3
"""Wordlister, a simple wordlist generator and mangler written in python 3.10.1."""
# Written By Ananke: https://github.com/4n4nk3

import argparse
from copy import copy
from itertools import permutations
from multiprocessing import Pool, current_process
from os import remove
from sys import exit, platform

if 'linux' in platform:
    from subprocess import Popen, PIPE


class Wordlister:
    LEET_TRANSLATIONS = str.maketrans('oOaAeEiIsS', '0044331155')

    def __init__(self, arguments):
        self.args = arguments


    def leet_and_append_and_prepend(self, line_leet: str) -> set:
        """
        Generator that returns the leeted version of a string and also returns it with applied prepend
        and append mutagens if required by user's parameters.

        :param line_leet: the string to be leeted
        :type line_leet: str
        :return result: set
        """

        line_leet = line_leet.translate(self.LEET_TRANSLATIONS)
        result: set = {line_leet + '\n',}
        if self.args.append is not None:
            result.add(f'{line_leet}{self.args.append}\n')
        if self.args.prepend is not None:
            result.add(f'{self.args.prepend}{line_leet}\n')
        return result


    def get_input_words(self, file_path: str) -> set:
        """
        Read input file and return a set of words containing them also capitalized and uppercased if needed.

        :param file_path: the path to the file with the user supplied wordlist
        :type file_path: str
        :return _: set
        """

        try:
            with open(file_path, 'r') as input_file:
                words = set(input_file.read().splitlines())
        except FileNotFoundError:
            print('Input file not found!\nExiting...\n')
            exit(1)
        
        # Apply capitalize mutagen and upper mutagen if needed
        prepped_words: set = copy(words)
        if self.args.cap is True or self.args.up is True:
            for word in words:
                if self.args.cap is True:
                    prepped_words.add(word.capitalize())
                if self.args.up is True:
                    prepped_words.add(word.upper())
                
        return prepped_words
    
    
    def printer(self, permutation: tuple) -> str:
        """
        Generate words from permutation applying append, prepend and, leet mutagens.
        The words are then written to a temporary file that's unique for each pool worker.

        :param perms: tuple containing a permutation of the word list that must be elaborated
        :type perms: tuple
        :return data: set
        """
        
        result = set()
        worker_pid = current_process().pid
        output_file = f'out_worker_{worker_pid}.txt'
        
        if len(set(map(str.lower, permutation))) != len(permutation):
            line_printer = ''.join(permutation)
            if self.args.min <= len(line_printer) <= self.args.max:
                result.add(line_printer + '\n')
                if self.args.append is not None and len(line_printer) + len(self.args.append) <= self.args.max:
                    result.add(f'{line_printer}{self.args.append}\n')
                if self.args.prepend is not None and len(line_printer) + len(self.args.prepend) <= self.args.max:
                    result.add(f'{self.args.prepend}{line_printer}\n')
                if self.args.leet is True:
                    result.update(self.leet_and_append_and_prepend(line_printer))
    
        with open(output_file, 'a') as f_out:
            f_out.writelines(result)
                   
        return output_file


    def run(self):
        input_words = self.get_input_words(self.args.input)
        with Pool(self.args.cores) as pool:
            for x in range(self.args.perm):
                output_iterable = pool.map(self.printer, permutations(input_words, x + 1))
        
        # Remove duplicates leveraging sets' properties
        output_files = set(output_iterable)
        
        # If we are on linux we leverage GNU tools to clean the output efficiently
        if 'linux' in platform:
            # read all workers' output files
            p1 = Popen(['cat', *output_files], stdout=PIPE)
            # sort the output of p1 and remove duplicated lines
            p2 = Popen(['sort', '-u', '-o', f'{self.args.output}'], stdin=p1.stdout, stdout=PIPE)
            p2.communicate()
        # else we do it with Python's sets
        else:
            uniq_output = set()
            with open(self.args.output, 'w') as f_out:
                for file in output_files:
                    with open(file, 'r') as f_in:
                        uniq_output.update(f_in.read().splitlines())
                
                for line in uniq_output:
                    f_out.write(line + '\n')
    
        for file in output_files:
            # delete file after copying it to final output file
            remove(file)

        print(f'\nOutput saved to "{self.args.output}"!\n')


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
    required.add_argument('--output', help='Output file name', required=True)
    required.add_argument('--perm', help='Max number of words to be combined on the same line',
                          required=True, type=int)
    required.add_argument('--min', help='Minimum generated password length', required=True,
                          type=int)
    required.add_argument('--max', help='Maximum generated password length', required=True,
                          type=int)
    # Optional arguments
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


if __name__ == '__main__':
    args = init_argparse().parse_args()
    wordlister = Wordlister(arguments=args)
    wordlister.run()
