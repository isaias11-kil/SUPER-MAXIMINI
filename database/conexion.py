import pyodbc

class ConexionDB:
    def __init__(self):
        # Update these with your actual SQL Server connection details
        self.server = 'localhost'
        self.database = 'SuperMaximiniDB'
        self.username = 'sa'
        self.password = 'your_password'

        # Connection string
        self.conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password};"
            # If using Windows Authentication instead of SQL Server Authentication:
            # f"Trusted_Connection=yes;"
        )

    def get_connection(self):
        try:
            conn = pyodbc.connect(self.conn_str)
            return conn
        except pyodbc.Error as e:
            print(f"Database connection error: {e}")
            return None
