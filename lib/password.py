import random

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


if __name__ == "__main__":
    print (generate_password(24))
    