import hashlib
import os
import ubinascii

def hash_password(password):
    """
    Hashes a password with a randomly generated salt using SHA-256.
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

# Example usage
password = "my_secure_password"

# Hash the password
hashed = hash_password(password)

print("hexed_password:", hashed)


# Verify the password
is_valid = verify_password(password, hashed)
print("Password is valid:", is_valid)