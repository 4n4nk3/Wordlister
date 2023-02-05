# Wordlister
A simple wordlist generator and mangler written in python 3.10.1.
It makes use of python multiprocessing capabilities in order to speed up his job.


### Supported permutations:
 - [x] Capital
 - [x] Upper
 - [x] 1337
 - [x] Append
 - [x] Prepend

### Additional functions:
 - [x] Multiprocessing
 - [x] Multicore
 - [x] Possibility to adjust cores/processes number manually.
 - [x] Each generated password doesn't contain same word twice.
 
### Preview:

```
usage: wordlister.py [-h] --input INPUT --perm PERM --min MIN --max MAX
                     [--test TEST] [--cores CORES] [--leet] [--cap] [--up]
                     [--append APPEND] [--prepend PREPEND]

A simple wordlist generator and mangler written in python.

optional arguments:
  -h, --help         show this help message and exit
  --cores CORES      Manually specify processes/cores pool that you want to
                     use
  --leet             Activate l33t mutagen
  --cap              Activate capitalize mutagen
  --up               Activate uppercase mutagen
  --append APPEND    Append chosen word (append 'word' to all passwords)
  --prepend PREPEND  Prepend chosen word (prepend 'word' to all passwords)

required arguments:
  --input INPUT      Input file name
  --output OUTPUT    Output file name
  --perm PERM        Max number of words to be combined on the same line
  --min MIN          Minimum generated password length
  --max MAX          Maximum generated password length
```


**_This project is for educational purposes only. Don't use it for illegal activities. I don't support nor condone illegal or unethical actions and I can't be held responsible for possible misuse of this software._**
