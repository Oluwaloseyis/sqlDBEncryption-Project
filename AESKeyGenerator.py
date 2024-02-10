import os
# Generate a 32-byte (256-bit) random AES key
def generate_key():
    aes_key = os.urandom(32)
    print(aes_key)
    return aes_key