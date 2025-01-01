import re
import logging

log = logging.getLogger(__name__)

def validate_password(password):
    """
    Validates a password to ensure it has at least:
    - One letter (lowercase or uppercase)
    - One digit
    - One punctuation character

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    
    has_letter = re.search(r'[a-zA-Z]', password)  # At least one letter
    has_digit = re.search(r'\d', password)        # At least one digit
    has_punctuation = re.search(r'[!@#$%^&*(),.?":{}|<>~`_]', password)  # Punctuation
    has_whitespace = re.search(r'\s', password)
    
    if has_letter and has_digit and has_punctuation and not has_whitespace and len(password) > 8:
        log.debug(f'validate {password}: True')
        return True
    log.debug(f'validate {password}: False')
    return False

def default_validation(value):
    return True


def validate_numbers(value):
    regex = re.compile("^\d+$")
    return True if regex.search(value) else False

def validate_hostname(hostname):
    ValidHostnameRegex="^[\w\.-]+$"
    regex = re.compile(ValidHostnameRegex)
    log.debug(f'validate {hostname}: {regex.search(hostname)}')
    return True if regex.search(hostname) else False

def validate_true(value):
    return (True)
