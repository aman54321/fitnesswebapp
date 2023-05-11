from django.test import TestCase

# Create your tests here.
for i in range(0,5):
    for j in range(0,5):
        print("*" ,end="")
    print()

for i in range(0,5):
    for j in range(0,5):
        if i == 0 or i == 4 or j == 0 or j == 4:
            print("*", end="")
        else:
            print(" ", end="")
    print()


n = 5
for i in range(1,n+1):
    for j in range(1,i+1):
        print("*", end="")
    print()

n = 5
for i in range(n):
    for j in range(1,n-i):
        print(" ", end="")
    for k in range(0,i+1):
        print("*", end="")
    print()

n = 5
for i in range(n):
    for j in range(0,n-i):
        print("*", end="")
    for k in range(1,i):
        print(" ", end="")
    print()

n = 5
for i in range(n):
    for j in range(0,i):
        print(" ", end="")
    for k in range(i+1,n+1):
        print("*", end="")
    print()

n = 5
for i in range(1,n+1):
    for j in range(n-i):
        print(" ", end="")
    for k in range(2*i-1):
        print("*", end="")
    print()


import random
import string

upper = string.ascii_uppercase
lower = string.ascii_lowercase
digits = string.digits
symbols = string.punctuation

# password generator function
def password_generator(size):
    chars = upper + lower + digits + symbols
    password = ''
    for i in range(size):
        password += random.choice(chars)
    return password

print(password_generator(8))
print(password_generator(12))