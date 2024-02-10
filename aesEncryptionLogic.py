from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
import base64

def encrypt_message(key, message):
    backend = default_backend()
    iv = b'\x00' * 16  # You should use a different IV for each encryption
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()

    padded_data = padder.update(message.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return base64.b64encode(ciphertext).decode()

def decrypt_message(key, encrypted_message):
    backend = default_backend()
    iv = b'\x00' * 16  # Same IV used for encryption
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

    ciphertext = base64.b64decode(encrypted_message)
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return unpadded_data.decode()

# Example usage:
key = b'wH\x84P\x9f\x19Vh\xc3\x19lF\xeb\xb8`\xf5\xb7\xdb\xd9\xf9\x8dc"X}\x0c\x1eu\x1d\xdb\x0e\xb4'
message = "Hello, AES encryption!"
encrypted_message = encrypt_message(key, message)
print("Encrypted message:", encrypted_message)
decrypted_message = decrypt_message(key, encrypted_message)
print("Decrypted message:", decrypted_message)
