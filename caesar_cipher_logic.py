def caesar_encrypt(plain_text, shift):
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

def caesar_decrypt(encrypted_text, shift):
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

# Example usage:
plain_text = "Oluwaloseyi@123"
shift = 5
encrypted_text = caesar_encrypt(plain_text, shift)
print("Encrypted text:", encrypted_text)
decrypted_text = caesar_decrypt(encrypted_text, shift)
print("Decrypted text:", decrypted_text)



decrypted_text = caesar_decrypt("tqzbfqtxjdn@678", shift)
print("Decrypted text:", decrypted_text)