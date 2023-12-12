import itertools

uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lowercase = 'abcdefghijklmnopqrstuvwxyz'
numbers = '0123456789'
special_chars = '!@#$%^&*()_-+=~`[]{}|\\:;"\'<>,.?/'

min_length = int(input("MIN Insira o comprimento mínimo da senha: "))
max_length = int(input("MAX Insira o comprimento máximo da senha: "))

use_uppercase = input("UPPER Incluir caracteres maiúsculos? (S/N): ").lower() == 's'
use_lowercase = input("LOWER Incluir caracteres minúsculos? (S/N): ").lower() == 's'
use_numbers = input("NUMBERS Incluir números? (S/N): ").lower() == 's'
use_special_chars = input("SPECIAL Incluir caracteres especiais? (S/N): ").lower() == 's'

chars = ''
if use_uppercase:
    chars += uppercase
if use_lowercase:
    chars += lowercase
if use_numbers:
    chars += numbers
if use_special_chars:
    chars += special_chars

passwords = []
for length in range(min_length, max_length + 1):
    for combination in itertools.product(chars, repeat=length):
        passwords.append(''.join(combination))

print("Senhas geradas:")
for password in passwords:
    print(password)