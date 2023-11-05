class EventosRepository:
    def __init__(self, connection):
        self.connection = connection

    def create_evento(self, tipo_evento, estado_evento, fecha, evidencia_fotografica, evidencia_textual, evidencia_documento, id_equipo):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO eventos (tipo_evento, estado_evento, fecha, evidencia_fotografica, evidencia_textual, evidencia_documento, id_equipo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (tipo_evento, estado_evento, fecha, evidencia_fotografica, evidencia_textual, evidencia_documento, id_equipo))

            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error al crear un evento:", str(e))
            return {"error": str(e)}

    def get_eventos_for_equipo(self, equipo_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM eventos WHERE id_equipo = %s;", (equipo_id,))
            eventos = cursor.fetchall()

            eventos_as_dicts = []
            column_names = [d[0] for d in cursor.description]
            for evento in eventos:
                evento_dict = dict(zip(column_names, evento))
                eventos_as_dicts.append(evento_dict)

            cursor.close()

            return eventos_as_dicts
        except Exception as e:
            print("Error al obtener eventos de la base de datos:", str(e))
            return {"error": str(e)}

