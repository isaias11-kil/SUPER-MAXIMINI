import os
import pyodbc
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env si existe
load_dotenv()

class ConexionBD:
    def __init__(self):
        self.use_docker = os.getenv("USE_DOCKER_DB", "False").lower() in ("true", "1", "t")
        self.database = os.getenv("DB_NAME", "SuperMaximiniDB")
        self.conexion = None

        if self.use_docker:
            self.server = os.getenv("DB_SERVER", "localhost,1433")
            self.user = os.getenv("DB_USER", "sa")
            self.password = os.getenv("DB_PASSWORD", "YourStrong!Passw0rd")
        else:
            self.server = os.getenv("LOCAL_DB_SERVER", r"ISAIAS\ISAIAS")

    def conectar(self):
        try:
            if self.use_docker:
                # Autenticación de SQL Server (Docker)
                # Requiere TrustServerCertificate=yes para la imagen mssql/server:2022-latest y superior
                conn_str = (
                    'DRIVER={ODBC Driver 17 for SQL Server};'
                    f'SERVER={self.server};'
                    f'DATABASE={self.database};'
                    f'UID={self.user};'
                    f'PWD={self.password};'
                    'TrustServerCertificate=yes;'
                )
            else:
                # Autenticación de Windows (Instancia local)
                conn_str = (
                    'DRIVER={ODBC Driver 17 for SQL Server};'
                    f'SERVER={self.server};'
                    f'DATABASE={self.database};'
                    'Trusted_Connection=yes;'
                )

            self.conexion = pyodbc.connect(conn_str)
            print("Conexión a SQL Server exitosa.")
            return self.conexion
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None

    def cerrar(self):
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada.")
