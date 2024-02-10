from test import HillCipher
import numpy as np

# Example key string
key_string = "HILL"  # You can use any string or list of characters as the key

# Create a HillCipher instance with the key string
cipher = HillCipher(key_string)

# Encrypt a message
message = "Hello Sekoni@123"
encrypted_message = cipher.encrypt(message)
print("Encrypted message:", encrypted_message)

# Decrypt the encrypted message
decrypted_message = cipher.decrypt(encrypted_message)
print("Decrypted message:", decrypted_message)
