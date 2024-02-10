from NewDBEncryptionPackage import DBEncryptionPackage
import numpy as np

# Define the encryption keys
#aes_key = b'\xbe\xde!$\x84/\x04t\xa01\xd8\xd7\x1aJgn\xef\xcc\xe4\x8f\xc5[E\xfa\xfc\xb5\x957\xd0H\xf7"'
hill_key = np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]])
caesar_shift = 3

# Instantiate the DBEncryptionPackage class with the same encryption keys and database connection details
db_encryptor = DBEncryptionPackage(
    dbname='northwind_sampledb',
    user='postgres',
    password='password',
    host='localhost',
    hill_key=hill_key,
    caesar_shift=caesar_shift
)

# Connect to the database
db_encryptor.connect_to_database()

# Specify the table name and column to retrieve encrypted data
table_name = 'public.customers'
columns_to_decrypt = ['company_name', 'phone']  # Specify the column where the data was encrypted

# Decrypt all columns of the sample table
decrypted_data = db_encryptor.decrypt_all_columns(table_name, columns_to_decrypt)

# Print decrypted data
for column, data in decrypted_data.items():
    print(f"Decrypted data for {column}: {data}")
