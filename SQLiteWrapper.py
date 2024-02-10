import sqlite3

class SQLiteWrapper:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("ingredients.db")

    def check_connection(self):
        try:
            self.conn.cursor()
            print("Database connected")
            return True
        except Exception as ex:
            print("Database connection failed")
            return False
        
    def close(self):
        self.conn.close()

if __name__ == '__main__':
    wrapper = SQLiteWrapper()
    wrapper.check_connection()
    wrapper.close()