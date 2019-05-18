# Wordlister
A simple wordlist generator and mangler written in python.
It makes use of python multiprocessing capabilities in order to speed up his job (CPU intensive).


### Supported permutations:
 - [x] Capital
 - [x] Upper
 - [x] 1337
 - [x] Append
 - [x] Prepend

### Additional functions:
 - [x] Test/Dry run
 - [x] Multiprocessing
 - [x] Multicore
 - [x] Possibility to adjust cores/processes number manually
 
### Preview:

```
usage: wordlister.py [-h] --input INPUT --perm PERM --min MIN --max MAX
                     [--test TEST] [--cores CORES] [--leet] [--cap] [--up]
                     [--append APPEND] [--prepend PREPEND]

A simple wordlist generator and mangler written in python.

optional arguments:
  -h, --help         show this help message and exit
  --test TEST        Output first N iterations (single process/core)
  --cores CORES      Manually specify processes/cores pool that you want to
                     use
  --leet             Activate l33t mutagen
  --cap              Activate capitalize mutagen
  --up               Activate uppercase mutagen
  --append APPEND    Append chosen word (append 'word' to all passwords)
  --prepend PREPEND  Append chosen word (prepend 'word' to all passwords)

required arguments:
  --input INPUT      Input file name
  --perm PERM        Max number of words to be combined on the same line
  --min MIN          Minimum generated password length
  --max MAX          Maximum generated password length
```


**_This project is for educational purposes only. Don't use it for illegal activities. I don't support nor condone illegal or unethical actions and I can't be held responsible for possible misuse of this software._**
