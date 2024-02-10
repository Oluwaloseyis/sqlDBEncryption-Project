import psycopg2
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
import base64

class EncryptionManager:
    def __init__(self, aes_key, caesar_shift):
        self.aes_key = aes_key
        self.caesar_shift = caesar_shift

    # Caesar Cipher encryption
    def caesar_encrypt(self, plain_text, shift):
        encrypted_text = ""
        for char in plain_text:
            if char.isalnum():  # Check if the character is alphanumeric
                if char.isalpha():
                    shifted = ord(char) + shift
                    if char.islower():
                        encrypted_char = chr((shifted - ord('a')) % 26 + ord('a'))
                    else:
                        encrypted_char = chr((shifted - ord('A')) % 26 + ord('A'))
                else:  # Numeric character
                    shifted = ord(char) + shift
                    encrypted_char = chr((shifted - ord('0')) % 10 + ord('0'))
            else:
                encrypted_char = char  # Non-alphanumeric characters remain unchanged
            encrypted_text += encrypted_char
        return encrypted_text

    # Caesar Cipher decryption
    def caesar_decrypt(self, encrypted_text, shift):
        decrypted_text = ""
        for char in encrypted_text:
            if char.isalnum():  # Check if the character is alphanumeric
                if char.isalpha():
                    shifted = ord(char) - shift
                    if char.islower():
                        decrypted_char = chr((shifted - ord('a')) % 26 + ord('a'))
                    else:
                        decrypted_char = chr((shifted - ord('A')) % 26 + ord('A'))
                else:  # Numeric character
                    shifted = ord(char) - shift
                    decrypted_char = chr((shifted - ord('0')) % 10 + ord('0'))
            else:
                decrypted_char = char  # Non-alphanumeric characters remain unchanged
            decrypted_text += decrypted_char
        return decrypted_text

    # AES encryption
    def encrypt_message(self, message):
        backend = default_backend()
        iv = b'\x00' * 16  # You should use a different IV for each encryption
        cipher = Cipher(algorithms.AES(self.aes_key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(message.encode()) + padder.finalize()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(ciphertext).decode()

    # AES decryption
    def decrypt_message(self, encrypted_message):
        backend = default_backend()
        iv = b'\x00' * 16  # Same IV used for encryption
        cipher = Cipher(algorithms.AES(self.aes_key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

        ciphertext = base64.b64decode(encrypted_message)
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

        return unpadded_data.decode()

    # Combined encryption process
    def combined_encrypt(self, message):
        # Encrypt with Caesar cipher
        caesar_cipher_text = self.caesar_encrypt(message, self.caesar_shift)
        # Encrypt with AES
        aes_cipher_text = self.encrypt_message(caesar_cipher_text)
        return aes_cipher_text

    # Combined decryption process
    def combined_decrypt(self, encrypted_message):
        # Decrypt with AES
        decrypted_caesar_cipher_text = self.decrypt_message(encrypted_message)
        # Decrypt with Caesar cipher
        decrypted_message = self.caesar_decrypt(decrypted_caesar_cipher_text, self.caesar_shift)
        return decrypted_message

    # Connect to PostgreSQL database and encrypt selected columns
    def encrypt_selected_columns(self, db_connection_params, table_name, columns_to_encrypt):
        try:
            connection = psycopg2.connect(**db_connection_params)
            cursor = connection.cursor()
            for column in columns_to_encrypt:
                cursor.execute(f"SELECT {column} FROM {table_name}")
                rows = cursor.fetchall()
                for row in rows:
                    original_value = row[0]
                    encrypted_value = self.combined_encrypt(original_value)
                    cursor.execute(f"UPDATE {table_name} SET {column} = %s WHERE {column} = %s",
                                   (encrypted_value, original_value))
            connection.commit()
            print("Encryption of selected columns successful.")
        except Exception as e:
            print("Error:", e)
        finally:
            if connection:
                cursor.close()
                connection.close()

    # Connect to PostgreSQL database and decrypt selected columns
    def decrypt_selected_columns(self, db_connection_params, table_name, columns_to_decrypt):
        try:
            connection = psycopg2.connect(**db_connection_params)
            cursor = connection.cursor()
            for column in columns_to_decrypt:
                cursor.execute(f"SELECT {column} FROM {table_name}")
                rows = cursor.fetchall()
                for row in rows:
                    encrypted_value = row[0]
                    decrypted_value = self.combined_decrypt(encrypted_value)
                    cursor.execute(f"UPDATE {table_name} SET {column} = %s WHERE {column} = %s",
                                   (decrypted_value, encrypted_value))
            connection.commit()
            print("Decryption of selected columns successful.")
        except Exception as e:
            print("Error:", e)
        finally:
            if connection:
                cursor.close()
                connection.close()



