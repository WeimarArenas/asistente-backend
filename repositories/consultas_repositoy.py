class ConsultasRepository:
    def __init__(self, connection):
        self.connection = connection 

    def get_consultas(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM nuevas_consultas")

            consultas = cursor.fetchall()

            # Convertir los resultados a una lista de diccionarios
            consultas_as_dicts = []
            column_names = [d[0] for d in cursor.description]
            for consulta in consultas:
                consulta_dict = dict(zip(column_names, consulta))
                consultas_as_dicts.append(consulta_dict)

            cursor.close()

            return consultas_as_dicts
        except Exception as e:
            print("Error al obtener las consultas:", str(e))
            return {"error": str(e)}

    def create_consulta(self, tipo_consulta, fecha):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO nuevas_consultas (tipo_consulta, fecha)
                VALUES (%s, %s);
            """, (tipo_consulta, fecha))

            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error al crear una nueva consulta:", str(e))
            self.connection.rollback()  # Revertir la transacción en caso de error
            return {"error": str(e)}
        finally:
            cursor.close()
