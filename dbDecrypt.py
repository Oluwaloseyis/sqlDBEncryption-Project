from DBEncryptionPackage import EncryptionManager

import psycopg2

db_connection_params = {
    "host": "localhost",
    "database": "northwind_sampledb",
    "user": "postgres",
    "password": "password"
}

table_name = "public.employees"

aes_key_table = 'public.AES_Key_Store'

try:
    # Connect to the database
    connection = psycopg2.connect(**db_connection_params)
    # Create a cursor
    cursor = connection.cursor()
    # Execute SQL query to insert the AES key into the AES_Key_Store table
    cursor.execute("SELECT aes_key from {} WHERE table_name = '{}' order by id desc limit 1".format(aes_key_table,table_name ))

    key_data = cursor.fetchall()

    print(key_data)

    aes_key = key_data[0][0]
    print(aes_key)
    # Commit the transaction
    connection.commit()
    print("AES key retrieved successfully.")

    cursor.close()

except (Exception, psycopg2.Error) as error:
    print("Error while retrieving AES key from the database:", error)

finally:
    # Close the cursor and connection
    if connection:
        cursor.close()
        connection.close()


#aes_key = b'\xeeu\x8d:b\xe7\x1b\xe4\x00\x03\x9fRg\x1c\xb2\x93\xc0\xa4\x87\xc1P\x02 \\\xa1\x19\x94\xabU\xbe\xbc_'
caesar_shift = 5
encryption_manager = EncryptionManager(aes_key, caesar_shift)

# Example usage of connecting to PostgreSQL database and encrypting selected columns
#columns_to_encrypt = ["first_name", "last_name"]
#encryption_manager.encrypt_selected_columns(db_connection_params, table_name, columns_to_encrypt)

# Example usage of connecting to PostgreSQL database and decrypting selected columns

columns_to_decrypt = ["first_name", "last_name"]

#columns_to_decrypt = ["ship_country"]
encryption_manager.decrypt_selected_columns(db_connection_params, table_name, columns_to_decrypt)


