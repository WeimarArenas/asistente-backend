class RegistroInvimaRepository:
    def __init__(self, connection):
        self.connection = connection

    def create_registro_invima(self, numero_registro, vigencia, fecha, evidencia_fotografica, evidencia_textual, evidencia_documento, id_equipo):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO registro_invima (numero_registro, vigencia, fecha, evidencia_fotografica, evidencia_textual, evidencia_documento, id_equipo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (numero_registro, vigencia, fecha, evidencia_fotografica, evidencia_textual, evidencia_documento, id_equipo))

            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error al crear un registro de Invima:", str(e))
            return {"error": str(e)}

    def get_registros_invima_for_equipo(self, equipo_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM registro_invima WHERE id_equipo = %s;", (equipo_id,))
            registros_invima = cursor.fetchall()

            registros_invima_as_dicts = []
            column_names = [d[0] for d in cursor.description]
            for registro_invima in registros_invima:
                registro_invima_dict = dict(zip(column_names, registro_invima))
                registros_invima_as_dicts.append(registro_invima_dict)

            cursor.close()

            return registros_invima_as_dicts
        except Exception as e:
            print("Error al obtener registros de Invima de la base de datos:", str(e))
            return {"error": str(e)}
