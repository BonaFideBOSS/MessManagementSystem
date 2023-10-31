import hashlib
import random


def encrypt_message(message):
    encrypted_message = hashlib.md5(message.encode()).hexdigest()
    return encrypted_message


def generate_otp():
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(characters) for _ in range(6))
