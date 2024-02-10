import numpy as np

class HillCipher:
    def __init__(self, key_size):
        self.key_matrix = self.generate_valid_key_matrix(key_size)
        self.inv_key_matrix = np.linalg.inv(self.key_matrix)

    def generate_valid_key_matrix(self, size):
        while True:
            key_matrix = np.random.permutation(np.eye(size, dtype=int))  # Generate a permutation matrix
            if np.linalg.det(key_matrix) % 26 != 0:
                return key_matrix

    def encrypt(self, plaintext):
        block_size = len(self.key_matrix)
        padded_plaintext = plaintext.upper() + 'X' * (block_size - (len(plaintext) % block_size))  # Pad the plaintext to be a multiple of block_size
        ciphertext = ""
        for i in range(0, len(padded_plaintext), block_size):
            block = padded_plaintext[i:i + block_size]
            block_indices = [ord(c) - ord('A') if 'A' <= c <= 'Z' else 26 + ord(c) - ord('0') if '0' <= c <= '9' else 36 if c == ' ' else 37 if c == '.' else 38 if c == ',' else 39 if c == '!' else 40 if c == '?' else 41 if c == '@' else 42 if c == '#' else -1 for c in block]  # Map characters to indices
            cipher_indices = np.dot(self.key_matrix, block_indices) % 43  # Modulo 43 for all characters
            ciphertext += ''.join(chr(idx + ord('A')) if idx < 26 else chr(idx - 26 + ord('0')) if idx < 36 else ' ' if idx == 36 else '.' if idx == 37 else ',' if idx == 38 else '!' if idx == 39 else '?' if idx == 40 else '@' if idx == 41 else '#' if idx == 42 else '?' for idx in cipher_indices)  # Convert indices back to characters
        return ciphertext

    def decrypt(self, ciphertext):
        block_size = len(self.key_matrix)
        plaintext = ""
        for i in range(0, len(ciphertext), block_size):
            block = ciphertext[i:i + block_size]
            block_indices = [ord(c) - ord('A') if 'A' <= c <= 'Z' else 26 + ord(c) - ord('0') if '0' <= c <= '9' else 36 if c == ' ' else 37 if c == '.' else 38 if c == ',' else 39 if c == '!' else 40 if c == '?' else 41 if c == '@' else 42 if c == '#' else -1 for c in block]  # Map characters to indices
            plain_indices = np.dot(self.inv_key_matrix, block_indices) % 43  # Modulo 43 for all characters
            plain_indices = plain_indices.astype(int)  # Cast to integers
            decrypted_block = ''.join(chr(idx + ord('a')) if idx < 26 else chr(idx - 26 + ord('0')) if idx < 36 else ' ' if idx == 36 else '.' if idx == 37 else ',' if idx == 38 else '!' if idx == 39 else '?' if idx == 40 else '@' if idx == 41 else '#' if idx == 42 else '?' for idx in plain_indices)  # Convert indices back to characters
            plaintext += decrypted_block
        return plaintext.rstrip('x').rstrip('X')  # Remove padding characters

# Example usage:
cipher = HillCipher(2)  # Specify the size of the key matrix (e.g., 2x2)
plaintext = "Hello, world! This is a message with spaces and special characters. 123"
#plaintext = "Thanoswillreturn@2024"
ciphertext = cipher.encrypt(plaintext)
print("Ciphertext:", ciphertext)

decrypted_text = cipher.decrypt(ciphertext)
print("Decrypted text:", decrypted_text)
