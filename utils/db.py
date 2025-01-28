from mysql.connector import Error
import mysql.connector
from dotenv import load_dotenv
import os

class Database:
    def __init__(self):
        load_dotenv() # Loading ENV variables
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PSWD")
        self.database = os.getenv("DB_NAME")
        self.auth_plugin = 'mysql_native_password'
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                user = self.user,
                passwd = self.password,
                database = self.database,
                auth_plugin = self.auth_plugin
            )
            print("[DB] Connection to server successful")
            return True
        except Error as e:
            print(f"An unexpected error ocurred: '{e}'")
            return False
    
    def query(self, query, values=None):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, values)
                self.connection.commit()
                return cursor.lastrowid  # or any other result you need
            except Error as e:
                print(f"An unexpected error occurred: '{e}'")
                return None
            finally:
                cursor.close()
        else:
            print("No connection to the database established.")
            return None
    
    def close(self):
        if self.connection:
            self.connection.close()
            print("[DB] Connection to server closed")