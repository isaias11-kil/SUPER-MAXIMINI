import bcrypt
from .conexion import ConexionBD

def validar_credenciales(nombre_usuario, contrasena_texto_plano):
    """
    Busca al usuario en la base de datos y valida su contraseña.
    Retorna (True, datos_usuario) si es correcto, (False, mensaje_error) en caso contrario.
    """
    db = ConexionBD()
    conn = db.conectar()

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

            # Verificar si la contraseña coincide directamente en texto plano (como fue insertada por el usuario)
            if isinstance(db_contrasena, str) and db_contrasena == contrasena_texto_plano:
                datos_usuario = {
                    'UsuarioID': usuario_id,
                    'NombreUsuario': db_usuario,
                    'NombreCompleto': nombre_completo,
                    'Rol': rol
                }
                return True, datos_usuario

            # Si no coincide en texto plano, intentar verificar usando bcrypt
            if isinstance(db_contrasena, str):
                db_contrasena_bytes = db_contrasena.encode('utf-8')
            else:
                db_contrasena_bytes = db_contrasena

            # Controlar que sea un hash bcrypt valido, si falla checkpw levantara un ValueError que atajamos en el except
            try:
                if bcrypt.checkpw(contrasena_texto_plano.encode('utf-8'), db_contrasena_bytes):
                    datos_usuario = {
                        'UsuarioID': usuario_id,
                        'NombreUsuario': db_usuario,
                        'NombreCompleto': nombre_completo,
                        'Rol': rol
                    }
                    return True, datos_usuario
            except ValueError:
                # Ocurre si db_contrasena_bytes no es un hash de bcrypt (por ejemplo, es un texto plano y la comparacion anterior fallo)
                pass

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
