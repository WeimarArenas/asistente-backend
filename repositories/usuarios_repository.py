from flask import request

class UsuariosRepository:
    def __init__(self, connection):
        self.connection = connection

    def get_verify_user(self, correo, clave):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, nombre, correo, verificado, administrador FROM usuarios WHERE correo = %s and clave = %s;", (correo, clave,))
            usuarios = cursor.fetchall()

            usuarios_as_dicts = []
            column_names = [d[0] for d in cursor.description]
            for usuario in usuarios:
                usuario_dict = dict(zip(column_names, usuario))
                usuarios_as_dicts.append(usuario_dict)

            cursor.close()

            if not correo or not clave:
                return {"error": "El correo y la clave son obligatorios"}

            return usuarios_as_dicts
        except Exception as e:
            print("Error al obtener los datos de la base de datos:", str(e))
            return {"error": str(e)}
        
        # crear un usuario
    def create_user(self, nombre, usuario, clave, correo, verificado=True, administrador=False):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nombre, usuario, clave, correo, verificado, administrador) VALUES (%s, %s, %s, %s, %s, %s);",
                (nombre, usuario, clave, correo, verificado, administrador)
            )
            self.connection.commit()
            cursor.close()

            return {"success": "Usuario creado correctamente"}

        except Exception as e:
            print("Error al insertar el usuario en la base de datos:", str(e))
            return {"error": str(e)}
        
        # verificar usuario
    def update_user_verification(self, correo, nueva_verificacion):
        try:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE usuarios SET verificado = %s WHERE correo = %s;", (nueva_verificacion, correo,))
            self.connection.commit()
            cursor.close()
            return {"success": "Verificación de usuario actualizada correctamente."}
        except Exception as e:
            print("Error al actualizar la verificación del usuario:", str(e))
            return {"error": str(e)}