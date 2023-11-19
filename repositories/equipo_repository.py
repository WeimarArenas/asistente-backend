class EquipoRepository:
    def __init__(self, connection):
        self.connection = connection

    def get_equipos(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT
                    e.id,
                    e.nombre,
                    e.marca,
                    e.modelo,
                    e.serie,
                    e.propietario,
                    e.fecha_fabricacion,
                    e.fecha_ingreso,
                    e.condicion_ingreso,
                    e.riesgo,
                    e.id_invima,
                    e.id_area,
                    a.nombre_area AS nombre_area
                FROM
                    equipo e
                JOIN
                    areas a ON e.id_area = a.id
                    """)
            equipos = cursor.fetchall()

            # Convierte los resultados a una lista de diccionarios
            equipos_as_dicts = []
            column_names = [d[0] for d in cursor.description]
            for equipo in equipos:
                equipo_dict = dict(zip(column_names, equipo))
                equipos_as_dicts.append(equipo_dict)

            cursor.close()

            return equipos_as_dicts
        except Exception as e:
            print("Error al obtener equipos de la base de datos:", str(e))
            return {"error": str(e)}

    def create_equipo(self, nombre, marca, modelo, serie, propietario, fecha_fabricacion, fecha_ingreso,
                      condicion_ingreso, riesgo, id_invima, id_area):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO equipo (nombre, marca, modelo, serie, propietario, fecha_fabricacion, fecha_ingreso, condicion_ingreso, riesgo, id_invima, id_area)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
            nombre, marca, modelo, serie, propietario, fecha_fabricacion, fecha_ingreso, condicion_ingreso, riesgo,
            id_invima, id_area))
            self.connection.commit()
            return cursor.lastrowid  # Devuelve el ID del nuevo equipo creado
        except Exception as e:
            print("Error al crear un equipo:", str(e))
            return {"error": str(e)}

    def update_equipo(self, equipo_id, nombre, marca, modelo, serie, propietario, fecha_fabricacion, fecha_ingreso,
                      condicion_ingreso, riesgo, id_invima, id_area):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE equipo
                SET nombre = %s, marca = %s, modelo = %s, serie = %s, propietario = %s,
                    fecha_fabricacion = %s, fecha_ingreso = %s, condicion_ingreso = %s,
                    riesgo = %s, id_invima = %s, id_area = %s
                WHERE id = %s
            """, (
            nombre, marca, modelo, serie, propietario, fecha_fabricacion, fecha_ingreso, condicion_ingreso, riesgo,
            id_invima, id_area, equipo_id))
            self.connection.commit()
            return True  # Devuelve True si la actualización fue exitosa
        except Exception as e:
            print("Error al actualizar un equipo:", str(e))
            return {"error": str(e)}

    def delete_equipo(self, equipo_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM equipo WHERE id = %s", (equipo_id,))
            self.connection.commit()
            return True
        except Exception as e:
            print("Error al eliminar un equipo:", str(e))
            return {"error": str(e)}

    def get_equipos_by_area(self, id_area):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM equipo WHERE id_area = %s", (id_area,))
            equipos = cursor.fetchall()

            # Convierte los resultados a una lista de diccionarios
            equipos_as_dicts = []
            column_names = [d[0] for d in cursor.description]
            for equipo in equipos:
                equipo_dict = dict(zip(column_names, equipo))
                equipos_as_dicts.append(equipo_dict)

            cursor.close()

            return equipos_as_dicts
        except Exception as e:
            print("Error al obtener equipos de la base de datos:", str(e))
            return {"error": str(e)}