import random, string, hashlib

STRETCHING = 5
PEPPER = "ea04c80bbacd4088a8f5b30576968dad"

def get_random_str(len : int) -> str:
    chars = [random.choice(string.ascii_letters + string.digits) for i in range(len)]
    return ''.join(chars)

def create_password() -> str:
    chars = [random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(12)]
    return ''.join(chars)

def to_password_hash(password : str, salt : string) -> str:
    sha512: str = salt + password + PEPPER
    for i in range(STRETCHING):
        sha512 = hashlib.sha512(sha512.encode()).hexdigest()
    return sha512