#!/usr/bin/python3
"""Wordlister, a simple wordlist generator and mangler written in python 3.10.1."""
# Written By Ananke: https://github.com/4n4nk3

import argparse
from copy import copy
from itertools import permutations
from sys import exit 

class Wordlister:
    LEET_TRANSLATIONS = str.maketrans('oOaAeEiIsS', '0044331155')

    def __init__(self, arguments):
        self.args = arguments
        self.wordlist = set()


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
    
    
    def printer(self, permutation: tuple):
        """
        Generate words from permutation applying append, prepend and, leet mutagens.
        The words are then added to the set which will contain all the generated words.

        :param perms: tuple containing a permutation of the word list that must be elaborated
        :type perms: tuple
        """
        
        if len(set(map(str.lower, permutation))) == len(permutation):
            line_printer = ''.join(permutation)
            if self.args.min <= len(line_printer) <= self.args.max:
                self.wordlist.add(line_printer + '\n')
                if self.args.append is not None and len(line_printer) + len(self.args.append) <= self.args.max:
                    self.wordlist.add(f'{line_printer}{self.args.append}\n')
                if self.args.prepend is not None and len(line_printer) + len(self.args.prepend) <= self.args.max:
                    self.wordlist.add(f'{self.args.prepend}{line_printer}\n')
                if self.args.leet is True:
                    self.wordlist.update(self.leet_and_append_and_prepend(line_printer))


    def run(self):
        input_words = self.get_input_words(self.args.input)
        for x in range(self.args.perm):
            for perm in permutations(input_words, x + 1):
                self.printer(perm)
        
        if self.args.sort is True:
            self.wordlist = sorted(self.wordlist, key=len)    
        with open(self.args.output, 'w') as f_out:
            f_out.writelines(self.wordlist)

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
    parser.add_argument('--leet', help='Activate l33t mutagen', action='store_true')
    parser.add_argument('--cap', help='Activate capitalize mutagen', action='store_true')
    parser.add_argument('--up', help='Activate uppercase mutagen', action='store_true')
    parser.add_argument('--append', help='Append chosen word (append \'word\' to all passwords)',
                        required=False)
    parser.add_argument('--prepend', help='Prepend chosen word (prepend \'word\' to all passwords)',
                        required=False)
    parser.add_argument('--sort', help='Sort the output in ascending order based on the word length',
                        action='store_true')
    return parser


if __name__ == '__main__':
    args = init_argparse().parse_args()
    wordlister = Wordlister(arguments=args)
    wordlister.run()
