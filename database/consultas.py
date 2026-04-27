import bcrypt
from .conexion import ConexionDB

def validar_credenciales(nombre_usuario, contrasena_texto_plano):
    """
    Busca al usuario en la base de datos y valida su contraseña.
    Retorna (True, datos_usuario) si es correcto, (False, mensaje_error) en caso contrario.
    """
    db = ConexionDB()
    conn = db.get_connection()

    if not conn:
        return False, "Error de conexión a la base de datos."

    try:
        cursor = conn.cursor()
        query = """
            SELECT UsuarioID, NombreUsuario, Contrasena, NombreCompleto, Rol, Estado
            FROM usuarios
            WHERE NombreUsuario = ?
        """
        cursor.execute(query, (nombre_usuario,))
        row = cursor.fetchone()

        if row:
            usuario_id, db_usuario, db_contrasena, nombre_completo, rol, estado = row

            if not estado:
                return False, "El usuario está inactivo."

            # Verificar la contraseña usando bcrypt
            # Nota: db_contrasena debe ser de tipo bytes para bcrypt, si viene como string, hay que codificarla
            if isinstance(db_contrasena, str):
                db_contrasena_bytes = db_contrasena.encode('utf-8')
            else:
                db_contrasena_bytes = db_contrasena

            if bcrypt.checkpw(contrasena_texto_plano.encode('utf-8'), db_contrasena_bytes):
                datos_usuario = {
                    'UsuarioID': usuario_id,
                    'NombreUsuario': db_usuario,
                    'NombreCompleto': nombre_completo,
                    'Rol': rol
                }
                return True, datos_usuario
            else:
                return False, "Contraseña incorrecta."
        else:
            return False, "Usuario no encontrado."

    except Exception as e:
        return False, f"Error al validar: {e}"
    finally:
        if conn:
            conn.close()

def generar_hash_password(contrasena_texto_plano):
    """
    Utilidad para generar el hash de una contraseña para guardar en la BD.
    """
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(contrasena_texto_plano.encode('utf-8'), salt)
    return hash_password.decode('utf-8')
