# Assignment 1: 
# Kunal Deore & Martina Koltenbaeck
# 
# -------------------------------------------
#

# Exercise 1

# Import the libraries
import math
import random
import re
from datetime import datetime

random.seed(datetime.now())
population = list(range(10001))
sample_sizes = [10, 20, 50, 100, 200, 500, 1000, 2500, 5000]

print("#Smples \t Mean \t Std.Err \t 95%LB \t 95%UP")
for n in sample_sizes:
    sample = random.sample(population, n)
    mean = sum(sample) / n
    sum_2 = 0.0
    for x in sample:
        sum_2 += (x - mean) ** 2.0
    standard_deviation = math.sqrt(sum_2 / (n-1))
    standard_error = standard_deviation / math.sqrt(n)
    print(f'{n:0>4d} \t {mean:.5f} \t {standard_error:.2f}'
          f'\t {mean - 2.0 * standard_error:.2f}\t{mean + 2.0 * standard_error:.2f}')

    
# Exercise 2

# Enter the plaintext to be encrypted and make the plaintext all lowercase
plaintext = input('Please enter a message? ').lower()

# Print the plaintext to the console
print('Plaintext: ' + plaintext)

# Enter a shift, must be an integer and can be positive, negative, or zero
shift = int(input('Please enter a shift? '))

# -------------------------------------------
# Algorithm: Encrypt via Caesar Cipher
letters = 'abcdefghijklmnopqrstuvwxyz'
numbers = '0123456789'
len_letters = len(letters)
len_numbers = len(numbers)

# Initialize an encrypted text as an empty string
encrypted = ''

# Iterative over all characters text as an empty string
for character in plaintext:
    # Get the index of the character which is either a letter or number
    index_letter = letters.find (character)
    index_number = numbers.find(character)
    # If a letter, shift
    if index_letter > -1:
        encrypted += letters[(index_letter + shift) % len_letters]
    # If a number, shift
    elif index_number > -1:
        encrypted += numbers[(index_number + shift) % len_numbers]
    # If neither a letter or number, do not shift
    else:
        encrypted += character
        
decrypted = ''

# Output: Encrypted
print('Encrypted: ' + encrypted)

# Algorithm: Decrypt via reverse Caesar Cipher
# Same as above, but the shift is negative
for character in encrypted:
    index_letter = letters.find(character)
    index_number = numbers.find(character)
    if index_letter > -1:
        decrypted += letters[index_letter - (shift % len_letters)]
    elif index_number > -1:
        decrypted += numbers[index_number - (shift % len_numbers)]
    else:
        decrypted += character

# Output: Decrypted, should be the plaintext
print('Decrypted: ' + decrypted)

# Exercise 3
import re

# Enter the plaintext to be encrypted and make the plaintext all lowercase
plaintext = str(input('Please enter a message? ').lower())

# Print the plaintext to the console
print('Plaintext: ' + plaintext)

# Enter a valid key such as the length of the plaintext is equal to key and make the key all lowercase
key = input('Please enter a key? ').lower()

# Print the key to the console
print('Key: ' + key)

# Loop for getting the length of the key same as plaintext 
while True:
    if len(key) != len(plaintext):
        key = key * int(len(plaintext) / len(key)) + key[0:int(len(plaintext) % len(key))]
        print("The letters in key have been repeated to match the length of the message")
        if key.isdigit() == True:
            print("The key contains digits. \nPlease enter a valid key!")
            key = input('Please enter a valid key? ')
        elif bool(re.search("[@_!#$%^&*()<>?/\|}{~:]", key)) == True:
            print("The key contains special characters. \nPlease enter a valid key!")
            key = input('Please enter a valid key? ')
        else:
            print("The key is devoid of digits and special characters! \nThank you for giving a valid key.")
            break
    else:
        print("The key matches the the length of the plaintext! ")
        if key.isdigit() == True:
            print("The key contains digits. \nPlease enter a valid key!")
            key = input('Please enter a valid key? ')
        elif bool(re.search("[@_!#$%^&*()<>?/\|}{~:]", key)) == True:
            print("The key contains special characters. \nPlease enter a valid key!")
            key = input('Please enter a valid key? ')
        else:
            print("The key is devoid of digits and special characters! \nThank you for giving a valid key.")
            break
        
# -------------------------------------------
# Algorithm: encrypt via Vigenère Cipher
letters = 'abcdefghijklmnopqrstuvwxyz'
len_letters = len(letters)

# Initialize an encrypted text as an empty string
encrypted = ''

# Iterative over all characters text as an empty string
for character in range(len(plaintext)):
    index_letter = letters.find(plaintext[character])
    if index_letter > -1:
        encrypted += letters[(letters.find(plaintext[character]) + letters.find(key[character])) % 26]
    else:
        encrypted += plaintext[character]
        
# Output: Encrypted
print("This is the encrypted message: ", encrypted)

# Initialize a decrypted text as an empty string
decrypted = ''

# Iterative over all characters text as an empty string
for character in range(len(encrypted)):
    index_letter = letters.find(encrypted[character])
    if index_letter > -1:
        decrypted += letters[(letters.find(encrypted[character]) - letters.find(key[character]) + 26) % 26]
    else:
        decrypted += encrypted[character]

# Output: Decrypted, should be the plaintext
print('This is the decrypted plaintext: ' + decrypted)
