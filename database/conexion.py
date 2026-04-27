import pyodbc

class ConexionBD:
    def __init__(self):
        # Datos exactos del servidor SQL
        self.server = r'ISAIAS\ISAIAS'
        self.database = 'SuperMaximiniDB'
        self.conexion = None

    def conectar(self):
        try:
            self.conexion = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                f'SERVER={self.server};'
                f'DATABASE={self.database};'
                'Trusted_Connection=yes;' # Se usa 'yes' porque es Autenticación de Windows
            )
            print("Conexión a SQL Server exitosa.")
            return self.conexion
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None

    def cerrar(self):
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada.")
