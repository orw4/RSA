# A program that shows how RSA encryption works
# Created on 16.04.2022

# This program contains 4 parts: choosing keys, encryption, decyption and breaking a decryption.
# It uses small numbers (The private keys are between 100-500), so it isn't safe, it shows how RSA works on smaller
# numbers and how it can be broken in small numbers

# Choosing keys - this part gives 2 options: letting the user choose his private key or choosing a random key. The
# private key has 2 prime numbers p and q and a number priv that is coprime to (p-1)(q-1). The program chooses p
# and q using an algorithm that checks whether or not they are prime in high probability. It chooses priv using
# euclids' algorithm for finding the maximal common divider. The public key has a number publ that is the inverse
# of priv module (p-1)(q-1) and a number prod = p * q

# Encryption and decryption - the program converts a string messsage into an integer message using ord() and chr()
# functions. It encrypts an int message m by computing m ^ publ module prod and decrypts an int encrypted message m
# by computing m ^ priv module prod. In order to sign the message or remove the signature of the encrypted message,
# the program encrypts message m from a to b by computing decr_a(encr_b(m)) and decrypts message m from a to b by
# computing decr_b(encr_a(m))

# Breaking a decryption - the program gets the public keys of the people who sent and received the message, and tries
# to find the private key of the receiver. It finds the key using an algorithm that finds the dividers of a number
# (public prod). This algorithm uses exponential time, so it is not efficient in big numbers, but the program uses
# numbers between 100-500. When it finds the key, it decryptes the message in the same way the decryption part
# decryptes a message

# Creates the private and the public encryption keys
def key():
    answer = int(input("Do you want to choose your private key by yourself(1) \n or do you want to use a random key(2)? "))
    if answer == 1:
        privateP = int(input("Enter a big prime number "))
        privateQ = int(input("Enter another big prime number "))
        numR = (privateP - 1) * (privateQ - 1)
        print("Enter a big number x so",numR,"and x are coprimes ")
        privatePriv = int(input(" "))
    else:
        privateP = prime()
        privateQ = prime()
        #print(privateP,privateQ)
        numR = (privateP - 1) * (privateQ - 1)
        privatePriv = coprime(numR)
        showKey = input("Do you want to know your private key? Answer 'yes' or 'no' ")
        if showKey == "yes":
            print("Your private key is (",privateP,",",privateQ,",",privatePriv,")")
    publicProd = privateP * privateQ
    publicPubl = euclids(privatePriv,numR)[1]
    print("Your public key is (",publicPubl,", ",publicProd,")")
    return (privateP,privateQ,privatePriv,publicPubl,publicProd)

# Returns a random number when the number and num are coprime
def coprime(num):
    while True:
        num1 = randint(minKey,maxKey)
        if euclids(num,num1)[0] == 1 and euclids(num,num1)[2] > 0:
            return num1

# Finds the maximal common divider c and numbers x and y when priv * x +r * y = c, returns x
# Used to finding public publ, so private priv * publ module R is 1
def euclids(priv,r):
    if r == 0:
        return [priv,1,0]
    else:
        answer = euclids(r,priv % r)
        return [answer[0],answer[2],answer[1] - priv // r * answer[2]]

# Returns two random big prime numbers
def prime():
    while True:
        num = randint(minKey,maxKey)
        if isPrime(num):
            return num

# Checks whether or not num is a prime number
def isPrime(num):
    for n in range(50):
        check = randint(2,num - 1)
        if check == num:
            pass
        if (check ** (num - 1)) % num != 1: # Fermat's theorem
            return False
        else:
            if (check ** 2) % num == 1 and check % num != 1 and check %num != num - 1:
                return False
    return True

# Encrypts a message or removes the signature from a message
def encr(num,publ,prod):
    return (num ** publ) % prod

# Decrypts a message or signs a message
def decr(num,p,q,priv):
    return (num ** priv) % (p * q)

# Encrypts the whole message
def encrWhole(text,publ,prod):
    encrypted = ""
    for char in text:
        encryptedChar = encr(ord(char),publ,prod)
        encrypted = encrypted + chr(encryptedChar)
    return encrypted

# Decrypts the whole message
def decrWhole(text,p,q,priv):
    decrypted = ""
    for char in text:
        decryptedChar = decr(ord(char),p,q,priv)
        decrypted = decrypted + chr(decryptedChar)
    return decrypted

# Finds the dividers of a given number
def findDividers(num):
    if num > maxKey ** 3:
        return {0}
    current = 1
    maximum = num
    dividers = set()
    while current <= maximum:
        if num % current == 0:
            dividers.add(current)
            dividers.add(num // current)
        maximum = num // current + 1
        current = current + 1
    return dividers

# Finds the private key using information about the public key
def findKey(publicPubl, publicProd):
    dividers = list(findDividers(publicProd) - {1,publicProd})
    try:
        p = dividers[0]
        q = dividers[1]
        r = (p - 1) * (q - 1)
        priv = euclids(publicPubl,r)[1]
        #print(p,q,priv)
        return [p,q,priv]
    except:
        print("Error, didn't find the private key")
        return [0,0,0]

from random import randint
minKey = 100
maxKey = 500
[privateP,privateQ,privatePriv,publicPubl,publicProd] = key()
#print(privateP,privateQ,privatePriv,publicPubl,publicProd)

def main(privateP,privateQ,privatePriv):
    answer = int(input("Do you want to encrypt a message(1), \n or do you want to decrypt a message(2), \n or do "
                       "you want to break other encryption(3)? "))
    if answer == 1:
        message = input("Enter the message you want to encrypt ")
        publ = int(input("Enter the first part of the public encryption key of whom you write to "))
        prod = int(input("Enter the second part of the public encryption key of whom you write to "))
        encrypted = encrWhole(message, publ, prod)
        print("Your encrypted, signed message is ", decrWhole(encrypted, privateP, privateQ, privatePriv))
    elif answer == 2:
        message = input("Enter the message you want to decrypt ")
        publ = int(input("Enter the first part of the public encryption key of the person who wrote to you "))
        prod = int(input("Enter the second part of the public encryption key of the person who wrote to you "))
        encrypted = encrWhole(message, publ, prod)
        print("The decrypted message is ", decrWhole(encrypted, privateP, privateQ, privatePriv))
    else:
        message = input("Enter the encrypted message you want to decrypt ")
        publSent = int(input("Enter the first part of the public encryption key of the person who wrote this "))
        prodSent = int(input("Enter the second part of the public encryption key of the person who wrote this "))
        publReceive = int(input("Enter the first part of the public encryption key of the person who is supposed to get this message "))
        prodReceive = int(input("Enter the second part of the public encryption key of the person who is supposed to get this message "))
        [p, q, priv] = findKey(publReceive,prodReceive)
        if [p,q,priv] != [0,0,0]:
            encrypted = encrWhole(message, publSent, prodSent)
            print("The decrypted message is ", decrWhole(encrypted, p, q, priv))
    continue0 = input("Do you want to use this program again? Answer 'yes' or 'no' ")
    if continue0 == "yes":
        new = input("Do you want to change your key? ")
        if new == "yes":
            [privateP, privateQ, privatePriv, publicPubl, publicProd] = key()
        main(privateP, privateQ, privatePriv)

main(privateP,privateQ,privatePriv)
