import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.host = 'localhost'
        self.db_name = 'perpustakaan'
        self.username = 'root'
        self.password = ''
        self.connection = None
        
    def get_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.db_name,
                user=self.username,
                password=self.password
            )
            if self.connection.is_connected():
                print("Connection to the database was successful.")
                return self.connection
        except Error as e:
            print(f"Error while connecting to the database: {e}")
            return None