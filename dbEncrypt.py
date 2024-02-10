from DBEncryptionPackage import EncryptionManager
from AESKeyGenerator import generate_key
import psycopg2

aes_key = generate_key()

caesar_shift = 5
encryption_manager = EncryptionManager(aes_key, caesar_shift)

# Example usage of connecting to PostgreSQL database and encrypting selected columns
db_connection_params = {
    "host": "localhost",
    "database": "northwind_sampledb",
    "user": "postgres",
    "password": "password"
}

table_name = "public.employees"
columns_to_encrypt = ["first_name", "last_name"]

#columns_to_encrypt = ["ship_country"]

encryption_manager.encrypt_selected_columns(db_connection_params, table_name, columns_to_encrypt)

# Example usage of connecting to PostgreSQL database and decrypting selected columns
###columns_to_decrypt = ["first_name", "last_name"]
###encryption_manager.decrypt_selected_columns(db_connection_params, table_name, columns_to_decrypt)

aes_key_table = 'public.AES_Key_Store'

try:
    # Connect to the database
    connection = psycopg2.connect(**db_connection_params)
    # Create a cursor
    cursor = connection.cursor()
    # Execute SQL query to insert the AES key into the AES_Key_Store table
    cursor.execute("INSERT INTO {} (table_name, aes_key) VALUES (%s, %s)".format(aes_key_table), (table_name,aes_key))
    # Commit the transaction
    connection.commit()
    print("AES key inserted successfully.")

except (Exception, psycopg2.Error) as error:
    print("Error while inserting AES key into the database:", error)

finally:
    # Close the cursor and connection
    if connection:
        cursor.close()
        connection.close()
