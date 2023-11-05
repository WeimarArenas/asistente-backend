class AreaRepository:
    def __init__(self, connection):
        self.connection = connection
    def area_exists(self, nombre_area):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM areas WHERE nombre_area = %s", (nombre_area,))
        count = cursor.fetchone()[0]
        cursor.close()
        return count > 0
    def get_areas(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM areas;")
            areas = cursor.fetchall()

            areas_as_dicts = []
            column_names = [d[0] for d in cursor.description]
            for area in areas:
                area_dict = dict(zip(column_names, area))
                areas_as_dicts.append(area_dict)

            cursor.close()

            return areas_as_dicts
        except Exception as e:
            print("Error al obtener equipos de la base de datos:", str(e))
            return {"error": str(e)}

    def create_area(self, nombre_area):
        if self.area_exists(nombre_area):
            return {"error": "El área ya existe"}
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO areas (nombre_area)
                VALUES (%s)
            """, (nombre_area,))

            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error al crear un area:", str(e))
            return {"error": str(e)}

    def delete_area(self, area_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM areas WHERE id = %s", (area_id,))
            self.connection.commit()
            return True
        except Exception as e:
            print("Error al eliminar el area:", str(e))
            return {"error": str(e)}
        