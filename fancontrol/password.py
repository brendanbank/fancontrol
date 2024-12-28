import random
import os
import hashlib
import ubinascii

ascii_lowercase = "abcdefghijklmnopqrstuvwxyz"
ascii_uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
punctuation = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
ascii_letters = ascii_lowercase + ascii_uppercase

def generate_password(lenght=12, num_digits=4, num_punctuation=2):

    password = ""
    
    for _ in range(lenght - num_digits - num_punctuation):
        password += random.choice(ascii_letters)
    
    for _ in range(num_digits):
        password += random.choice(digits)
        
    for _ in range(num_punctuation):
        password += random.choice(punctuation)

    shuffle = { key: password[key] for key in range(len(password)) }
    shuffle_password = ""
    
    for i in range(len(password)):
        number = random.choice([ key for key in shuffle.keys() ])
        shuffle_password += password[number]
        del (shuffle[number])
        
    return(shuffle_password)

def hash_password(password):
    """
    Hashes a password with a randomly generated salt using SHA-512.
    Returns the salt and the hashed password.
    """
    # Generate a random 16-byte salt
    salt = os.urandom(16)
    
    # Combine salt and password
    password_bytes = password.encode('utf-8')
    salted_password = salt + password_bytes
    
    # Hash the salted password using SHA-256
    hash_object = hashlib.sha512(salted_password)
    hashed_password = hash_object.digest()  # Get raw binary hash
    
    salt_hex = ubinascii.hexlify(salt).decode('utf-8')
    hash_hex = ubinascii.hexlify(hashed_password).decode('utf-8')
    return f"{salt_hex}${hash_hex}"

def verify_password(password, hexed_password):
    """
    Verifies a password against a given salt and hashed password.
    """
    salt, hashed = hexed_password.split('$')
    salt = ubinascii.unhexlify(salt)
    hashed_password = ubinascii.unhexlify(hashed)

    # Combine the salt and the password to hash again
    password_bytes = password.encode('utf-8')
    salted_password = salt + password_bytes
    
    # Hash the salted password
    hash_object = hashlib.sha512(salted_password)
    return hash_object.digest() == hashed_password

if __name__ == "__main__":
    password = "secret"
    hashed_password = hash_password(password)
    print (hashed_password)
    print (verify_password(password, hashed_password))

if __name__ == "__main__":
    print (generate_password(24))
    