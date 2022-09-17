# A program that shows how RSA encryption works
# 16.04.2022

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
    publicProd = privateP * privateQ
    publicPubl = euclids(privatePriv,numR)[1]
    print("Your public key is (",publicPubl,", ",publicProd,")")
    return (privateP,privateQ,privatePriv,publicPubl,publicProd)

# Returns a random number when the number and num are coprime
def coprime(num):
    while True:
        num1 = randint(100,500)
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
        num = randint(100,500)
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

from random import randint
[privateP,privateQ,privatePriv,publicPubl,publicProd] = key()
#print(privateP,privateQ,privatePriv,publicPubl,publicProd)
answer = int(input("Do you want to encrypt a message(1), \n or do you want to decrypt a message(2)? "))
if answer == 1:
    message = input("Enter the message you want to encrypt ")
    publ = int(input("Enter the first part of the public encryption key of whom you write to "))
    prod = int(input("Enter the second part of the public encryption key of whom you write to "))
    encrypted = encrWhole(message,publ,prod)
    print("Your encrypted, signed message is ",decrWhole(encrypted,privateP,privateQ,privatePriv))
else:
    message = input("Enter the message you want to decrypt ")
    publ = int(input("Enter the first part of the public encryption key of the person who wrote to you "))
    prod = int(input("Enter the second part of the public encryption key of the person who wrote to you "))
    encrypted = encrWhole(message,publ,prod)
    print("The decrypted message is ",decrWhole(encrypted,privateP,privateQ,privatePriv))