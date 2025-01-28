from mysql.connector import Error
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv() # Loading ENV variables

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PSWD"),
            database=os.getenv("DB_NAME")
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# Example usage:
# connection = create_connection("localhost", "root", "password", "database_name")