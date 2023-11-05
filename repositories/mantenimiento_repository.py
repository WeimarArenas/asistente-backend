class MantenimientosRepository:
    def __init__(self, connection):
        self.connection = connection

    def create_mantenimiento(self, tipo_mantenimiento, estado, fecha, evidencia_fotografica, evidencia_textual, evidencia_documento, id_equipo):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO mantenimientos (tipo_mantenimiento, estado, fecha, evidencia_fotografica, evidencia_textual, evidencia_documento, id_equipo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (tipo_mantenimiento, estado, fecha, evidencia_fotografica, evidencia_textual, evidencia_documento, id_equipo))

            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error al crear un mantenimiento:", str(e))
            return {"error": str(e)}

    def get_mantenimientos_for_equipo(self, equipo_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM mantenimientos WHERE id_equipo = %s;", (equipo_id,))
            mantenimientos = cursor.fetchall()

            mantenimientos_as_dicts = []
            column_names = [d[0] for d in cursor.description]
            for mantenimiento in mantenimientos:
                mantenimiento_dict = dict(zip(column_names, mantenimiento))
                mantenimientos_as_dicts.append(mantenimiento_dict)

            cursor.close()

            return mantenimientos_as_dicts
        except Exception as e:
            print("Error al obtener mantenimientos de la base de datos:", str(e))
            return {"error": str(e)}
