from mysql.connector import Error
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv() # Loading ENV variables

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PSWD"),
            database=os.getenv("DB_NAME"),
            auth_plugin='mysql_native_password'
        )
        print("[DB] Connection to server successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection