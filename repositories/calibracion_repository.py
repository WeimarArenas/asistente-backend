class CalibracionesRepository:
    def __init__(self, connection):
        self.connection = connection

    def get_calibraciones_for_equipo(self, equipo_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM calibraciones WHERE id_equipo = %s;", (equipo_id,))
            calibraciones = cursor.fetchall()

            calibraciones_as_dicts = []
            column_names = [d[0] for d in cursor.description]
            for calibracion in calibraciones:
                calibracion_dict = dict(zip(column_names, calibracion))
                calibraciones_as_dicts.append(calibracion_dict)

            cursor.close()

            return calibraciones_as_dicts
        except Exception as e:
            print("Error al obtener calibraciones de la base de datos:", str(e))
            return {"error": str(e)}

    def create_calibracion(self, estado, fecha, evidencia_fotografica, evidencia_textual, evidencia_documento, id_equipo):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO calibraciones (estado, fecha, evidencia_fotografica, evidencia_textual, evidencia_documento, id_equipo)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (estado, fecha, evidencia_fotografica, evidencia_textual, evidencia_documento, id_equipo))

            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error al crear una calibración:", str(e))
            return {"error": str(e)}


