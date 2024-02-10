from NewDBEncryptionPackage import DBEncryptionPackage
import numpy as np

# Define the encryption keys
#aes_key = b'\xbe\xde!$\x84/\x04t\xa01\xd8\xd7\x1aJgn\xef\xcc\xe4\x8f\xc5[E\xfa\xfc\xb5\x957\xd0H\xf7"'
hill_key = np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]])
caesar_shift = 3

# Instantiate the DBEncryptionPackage class
db_encryptor = DBEncryptionPackage(
    dbname='northwind_sampledb',
    user='postgres',
    password='password',
    host='localhost',
    hill_key=hill_key,
    caesar_shift=caesar_shift
)

# Specify the table name and columns to be encrypted
table_name = 'public.customers'
#columns_to_encrypt = ['company_name', 'contact_name', 'postal_code']  # Add all column names here
columns_to_encrypt = ['company_name', 'phone']

# Encrypt all columns of the sample table
db_encryptor.encrypt_all_columns(table_name, columns_to_encrypt)