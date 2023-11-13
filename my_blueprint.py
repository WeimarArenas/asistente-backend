from MySQLdb import OperationalError
from flask import Blueprint, jsonify, request

my_blueprint = Blueprint('my_blueprint', __name__)

# Get --> Traer
# Post --> Crear
# Put --> Editar
# Delete --> Eliminar
@my_blueprint.route('/equipos', methods=['GET'])
def get_equipos_route():
    from repositories.equipo_repository import EquipoRepository
    from app import mysql  # Importa la conexión aquí solo para esta función
    try:
        equipo_repository = EquipoRepository(mysql.connection)
        equipos = equipo_repository.get_equipos()

        # Formatea los datos a una lista de diccionarios
        formatted_equipos = []

        for equipo in equipos:
            formatted_equipo = {
                "id": equipo["id"],
                "nombre": equipo["nombre"],
                "marca": equipo["marca"],
                "modelo": equipo["modelo"],
                "serie": equipo["serie"],
                "propietario": equipo["propietario"],
                "condicion_ingreso": equipo["condicion_ingreso"],
                "riesgo": equipo["riesgo"],
                "id_invima": equipo["id_invima"],
                "id_area": equipo["id_area"]
            }

            if equipo["fecha_fabricacion"] is not None:
                formatted_equipo["fecha_fabricacion"] = equipo["fecha_fabricacion"].strftime("%Y-%m-%d")
            else:
                formatted_equipo["fecha_fabricacion"] = None  # o asigna otro valor por defecto si prefieres

            if equipo["fecha_ingreso"] is not None:
                formatted_equipo["fecha_ingreso"] = equipo["fecha_ingreso"].strftime("%Y-%m-%d")
            else:
                formatted_equipo["fecha_ingreso"] = None  # o asigna otro valor por defecto si prefieres

            formatted_equipos.append(formatted_equipo)

        return jsonify({'equipos': formatted_equipos})
    except OperationalError as e:
        # Manejo de error de base de datos
        print(f"Error de base de datos: {str(e)}")
        return jsonify({'error': 'Error en la base de datos'})

@my_blueprint.route('/equipos', methods=['POST'])
def create_equipo_route():
    from repositories.equipo_repository import EquipoRepository
    from app import mysql  # Importa la conexión aquí solo para esta función

    data = request.get_json()

    if not data:
        return jsonify({'error': 'Datos no proporcionados en el cuerpo de la solicitud'}), 400

    nombre = data.get("nombre")
    marca = data.get("marca")
    modelo = data.get("modelo")
    serie = data.get("serie")
    propietario = data.get("propietario")
    fecha_fabricacion = data.get("fecha_fabricacion")
    fecha_ingreso = data.get("fecha_ingreso")
    condicion_ingreso = data.get("condicion_ingreso")
    riesgo = data.get("riesgo")
    id_invima = data.get("id_invima")
    id_area = data.get("id_area")

    # Crea una instancia de EquipoRepository
    equipo_repository = EquipoRepository(mysql.connection)  # Asegúrate de que `mysql` esté configurado correctamente

    # Llama a la función para crear un equipo
    equipo_id = equipo_repository.create_equipo(nombre, marca, modelo, serie, propietario, fecha_fabricacion,
                                                fecha_ingreso, condicion_ingreso, riesgo, id_invima, id_area)

    if isinstance(equipo_id, int):
        return jsonify({'message': 'Equipo creado exitosamente', 'equipo_id': equipo_id}), 201
    else:
        return jsonify({'error': 'Error al crear el equipo', 'details': equipo_id}), 500

@my_blueprint.route('/equipos/<int:equipo_id>', methods=['PUT'])
def update_equipo_route(equipo_id):
    from repositories.equipo_repository import EquipoRepository
    from app import mysql  # Importa la conexión aquí solo para esta función

    data = request.get_json()
    nombre = data.get("nombre")
    marca = data.get("marca")
    # ... otros campos ...

    # Crea una instancia de EquipoRepository
    equipo_repository = EquipoRepository(mysql.connection)

    # Llama a la función para actualizar un equipo
    success = equipo_repository.update_equipo(equipo_id, nombre, marca, ...)  # Pasa todos los campos necesarios

    if success:
        return jsonify({'message': 'Equipo actualizado exitosamente'}), 200
    else:
        return jsonify({'error': 'Error al actualizar el equipo'}), 500

@my_blueprint.route('/equipos/<int:equipo_id>', methods=['DELETE'])
def delete_equipo_route(equipo_id):
    from repositories.equipo_repository import EquipoRepository
    from app import mysql  # Importa la conexión aquí solo para esta función
    # Crea una instancia de EquipoRepository
    equipo_repository = EquipoRepository(mysql.connection)

    # Llama a la función para eliminar un equipo
    success = equipo_repository.delete_equipo(equipo_id)

    if success:
        return jsonify({'message': 'Equipo eliminado exitosamente'}), 200
    else:
        return jsonify({'error': 'Error al eliminar el equipo'}), 500

# rutas para las solicitudes de las areas
@my_blueprint.route('/areas', methods=['GET'])
def get_areas_route():
    from repositories.areas_repository import AreaRepository
    from app import mysql
    try:
        area_repository = AreaRepository(mysql.connection)
        areas = area_repository.get_areas()
        formatted_areas = []

        for area in areas:
            formatted_areas.append({
                "id": area["id"],
                "nombre_area": area["nombre_area"]
            })

        return jsonify({'areas': formatted_areas})
    except OperationalError as e:

        print(f"Error de base de datos: {str(e)}")
        return jsonify({'error': 'Error en la base de datos'})

@my_blueprint.route('/areas', methods=['POST'])
def create_area_route():
    from repositories.areas_repository import AreaRepository
    from app import mysql

    data = request.get_json()

    if not data:
        return jsonify({'error': 'Datos no proporcionados en el cuerpo de la solicitud'}), 400

    nombre_area = data.get("nombre_area")

    area_repository = AreaRepository(mysql.connection)
    result = area_repository.create_area(nombre_area)

    if isinstance(result, int):  # Verifica si es un entero (ID)
        return jsonify({'message': 'area creada exitosamente', 'nombre_area_id': result}), 201
    else:
        return jsonify({'error': 'Error al crear el area', 'details': result['error']}), 500

    @my_blueprint.route('/equipos/<int:equipo_id>', methods=['DELETE'])
    def delete_equipo_route(equipo_id):
        from repositories.equipo_repository import EquipoRepository
        from app import mysql  # Importa la conexión aquí solo para esta función
        # Crea una instancia de EquipoRepository
        equipo_repository = EquipoRepository(mysql.connection)

        # Llama a la función para eliminar un equipo
        success = equipo_repository.delete_equipo(equipo_id)

        if success:
            return jsonify({'message': 'Equipo eliminado exitosamente'}), 200
        else:
            return jsonify({'error': 'Error al eliminar el equipo'}), 500

@my_blueprint.route('/areas/<int:area_id>', methods=['DELETE'])
def delete_area_route(area_id):
    from repositories.areas_repository import AreaRepository
    from app import mysql
    area_repository = AreaRepository(mysql.connection)

    success = area_repository.delete_area(area_id)

    if success:
        return jsonify({'message': 'Area eliminada exitosamente'}), 200
    else:
        return jsonify({'error': 'Error al eliminar el area'}), 500

@my_blueprint.route('/areas/equipos/<int:id_area>', methods=['GET'])
def get_equipos_by_area(id_area):
    from repositories.equipo_repository import EquipoRepository
    from app import mysql  # Importa la conexión aquí solo para esta función
    try:
        equipo_repository = EquipoRepository(mysql.connection)
        equipos = equipo_repository.get_equipos_by_area(id_area)

        # Formatea los datos a una lista de diccionarios
        formatted_equipos = []

        for equipo in equipos:
            formatted_equipo = {
                "id": equipo["id"],
                "nombre": equipo["nombre"],
                "marca": equipo["marca"],
                "modelo": equipo["modelo"],
                "serie": equipo["serie"],
                "propietario": equipo["propietario"],
                "condicion_ingreso": equipo["condicion_ingreso"],
                "riesgo": equipo["riesgo"],
                "id_invima": equipo["id_invima"],
                "id_area": equipo["id_area"]
            }

            if equipo["fecha_fabricacion"] is not None:
                formatted_equipo["fecha_fabricacion"] = equipo["fecha_fabricacion"].strftime("%Y-%m-%d")
            else:
                formatted_equipo["fecha_fabricacion"] = None  # o asigna otro valor por defecto si prefieres

            if equipo["fecha_ingreso"] is not None:
                formatted_equipo["fecha_ingreso"] = equipo["fecha_ingreso"].strftime("%Y-%m-%d")
            else:
                formatted_equipo["fecha_ingreso"] = None  # o asigna otro valor por defecto si prefieres

            formatted_equipos.append(formatted_equipo)

        return jsonify({'equipos': formatted_equipos})
    except OperationalError as e:
        # Manejo de error de base de datos
        print(f"Error de base de datos: {str(e)}")
        return jsonify({'error': 'Error en la base de datos'})

# rutas calibraciones
@my_blueprint.route('/equipos/calibraciones/<int:equipo_id>', methods=['GET'])
def get_calibracion_equipo_route(equipo_id):
    from repositories.calibracion_repository import CalibracionesRepository
    from app import mysql  # Importa la conexión aquí solo para esta función

    try:
        calibraciones_repository = CalibracionesRepository(mysql.connection)
        calibraciones = calibraciones_repository.get_calibraciones_for_equipo(equipo_id)

        if isinstance(calibraciones, list):
            return jsonify({'calibraciones': calibraciones}), 200
        else:
            return jsonify({'error': 'Error al obtener calibraciones', 'details': calibraciones['error']}), 500
    except OperationalError as e:
        # Manejo de error de base de datos
        print(f"Error de base de datos: {str(e)}")
        return jsonify({'error': 'Error de base de datos'})

@my_blueprint.route('/equipos/calibraciones', methods=['POST'])
def create_calibracion_route():
    from repositories.calibracion_repository import CalibracionesRepository
    from app import mysql

    data = request.get_json()

    if not data:
        return jsonify({'error': 'Datos no proporcionados en el cuerpo de la solicitud'}), 400

    estado = data.get("estado")
    fecha = data.get("fecha")
    evidencia_fotografica = data.get("evidencia_fotografica")
    evidencia_textual = data.get("evidencia_textual")
    evidencia_documento = data.get("evidencia_documento")
    id_equipo = data.get("id_equipo")

    if estado is None or fecha is None or evidencia_fotografica is None or id_equipo is None:
        return jsonify({'error': 'Datos incompletos para crear una calibración'}), 400

    calibraciones_repository = CalibracionesRepository(mysql.connection)

    result = calibraciones_repository.create_calibracion(estado, fecha, evidencia_fotografica, evidencia_textual, evidencia_documento, id_equipo)

    if isinstance(result, int):
        return jsonify({'message': 'Calibración creada exitosamente', 'calibracion_id': result}), 201
    else:
        return jsonify({'error': 'Error al crear la calibración', 'details': result['error']}), 500


# Rutas para los eventos
@my_blueprint.route('/equipos/eventos', methods=['POST'])
def create_evento_route():
    from repositories.evento_repository import EventosRepository
    from app import mysql

    data = request.get_json()

    if not data:
        return jsonify({'error': 'Datos no proporcionados en el cuerpo de la solicitud'}), 400

    tipo_evento = data.get("tipo_evento")
    estado_evento = data.get("estado_evento")
    fecha = data.get("fecha")
    evidencia_fotografica = data.get("evidencia_fotografica")
    evidencia_textual = data.get("evidencia_textual")
    evidencia_documento = data.get("evidencia_documento")
    id_equipo = data.get("id_equipo")

    if tipo_evento is None or fecha is None or id_equipo is None:
        return jsonify({'error': 'Datos incompletos para crear un evento'}), 400

    eventos_repository = EventosRepository(mysql.connection)

    result = eventos_repository.create_evento(tipo_evento, estado_evento, fecha, evidencia_fotografica, evidencia_textual, evidencia_documento, id_equipo)

    if isinstance(result, int):
        return jsonify({'message': 'Evento creado exitosamente', 'evento_id': result}), 201
    else:
        return jsonify({'error': 'Error al crear el evento', 'details': result['error']}), 500

@my_blueprint.route('/equipos/eventos/<int:equipo_id>', methods=['GET'])
def get_eventos_equipo_route(equipo_id):
    from repositories.evento_repository import EventosRepository
    from app import mysql

    try:
        eventos_repository = EventosRepository(mysql.connection)
        eventos = eventos_repository.get_eventos_for_equipo(equipo_id)

        if isinstance(eventos, list):
            return jsonify({'eventos': eventos}), 200
        else:
            return jsonify({'error': 'Error al obtener eventos', 'details': eventos['error']}), 500
    except OperationalError as e:
        # Manejo de error de base de datos
        print(f"Error de base de datos: {str(e)}")
        return jsonify({'error': 'Error de base de datos'})

#rutas para mantenimientos
@my_blueprint.route('/equipos/mantenimientos', methods=['POST'])
def create_mantenimiento_route():
    from repositories.mantenimiento_repository import MantenimientosRepository
    from app import mysql

    data = request.get_json()

    if not data:
        return jsonify({'error': 'Datos no proporcionados en el cuerpo de la solicitud'}), 400

    tipo_mantenimiento = data.get("tipo_mantenimiento")
    estado = data.get("estado")
    fecha = data.get("fecha")
    evidencia_fotografica = data.get("evidencia_fotografica")
    evidencia_textual = data.get("evidencia_textual")
    evidencia_documento = data.get("evidencia_documento")
    id_equipo = data.get("id_equipo")

    if tipo_mantenimiento is None or fecha is None or id_equipo is None:
        return jsonify({'error': 'Datos incompletos para crear un mantenimiento'}), 400

    mantenimientos_repository = MantenimientosRepository(mysql.connection)

    result = mantenimientos_repository.create_mantenimiento(tipo_mantenimiento, estado, fecha, evidencia_fotografica, evidencia_textual, evidencia_documento, id_equipo)

    if isinstance(result, int):
        return jsonify({'message': 'Mantenimiento creado exitosamente', 'mantenimiento_id': result}), 201
    else:
        return jsonify({'error': 'Error al crear el mantenimiento', 'details': result['error']}), 500

@my_blueprint.route('/equipos/mantenimientos/<int:equipo_id>', methods=['GET'])
def get_mantenimientos_equipo_route(equipo_id):
    from repositories.mantenimiento_repository import MantenimientosRepository
    from app import mysql

    try:
        mantenimientos_repository = MantenimientosRepository(mysql.connection)
        mantenimientos = mantenimientos_repository.get_mantenimientos_for_equipo(equipo_id)

        if isinstance(mantenimientos, list):
            return jsonify({'mantenimientos': mantenimientos}), 200
        else:
            return jsonify({'error': 'Error al obtener mantenimientos', 'details': mantenimientos['error']}), 500
    except OperationalError as e:
        # Manejo de error de base de datos
        print(f"Error de base de datos: {str(e)}")
        return jsonify({'error': 'Error de base de datos'})

# Rutas para registro invima
@my_blueprint.route('/equipos/registros-invima', methods=['POST'])
def create_registro_invima_route():
    from repositories.registro_invima_repository import RegistroInvimaRepository
    from app import mysql

    data = request.get_json()

    if not data:
        return jsonify({'error': 'Datos no proporcionados en el cuerpo de la solicitud'}), 400

    numero_registro = data.get("numero_registro")
    vigencia = data.get("vigencia")
    fecha = data.get("fecha")
    evidencia_fotografica = data.get("evidencia_fotografica")
    evidencia_textual = data.get("evidencia_textual")
    evidencia_documento = data.get("evidencia_documento")
    id_equipo = data.get("id_equipo")

    if numero_registro is None or vigencia is None or fecha is None or id_equipo is None:
        return jsonify({'error': 'Datos incompletos para crear un registro de Invima'}), 400

    registro_invima_repository = RegistroInvimaRepository(mysql.connection)

    result = registro_invima_repository.create_registro_invima(numero_registro, vigencia, fecha, evidencia_fotografica, evidencia_textual, evidencia_documento, id_equipo)

    if isinstance(result, int):
        return jsonify({'message': 'Registro de Invima creado exitosamente', 'registro_invima_id': result}), 201
    else:
        return jsonify({'error': 'Error al crear el registro de Invima', 'details': result['error']}), 500

@my_blueprint.route('/equipos/registros-invima/<int:id>', methods=['GET'])
def get_registros_invima_equipo_route(id):
    from repositories.registro_invima_repository import RegistroInvimaRepository
    from app import mysql

    try:
        registro_invima_repository = RegistroInvimaRepository(mysql.connection)
        registros_invima = registro_invima_repository.get_registros_invima_for_equipo(id)

        if isinstance(registros_invima, list):
            return jsonify({'registros_invima': registros_invima}), 200
        else:
            return jsonify({'error': 'Error al obtener registros de Invima', 'details': registros_invima['error']}), 500
    except OperationalError as e:
        # Manejo de error de base de datos
        print(f"Error de base de datos: {str(e)}")
        return jsonify({'error': 'Error de base de datos'})

# rutas para el manejo de usuarios
@my_blueprint.route('/usuarios/<string:correo>/<string:clave>', methods=['GET'])
def get_user_route(correo, clave):
    from repositories.usuarios_repository import UsuariosRepository
    from app import mysql
    
    try:
        usuarios_repository = UsuariosRepository(mysql.connection)
        usuarios = usuarios_repository.get_verify_user(correo, clave)

        if isinstance(usuarios, list):
            return jsonify({'usuario': usuarios}), 200
        else:
            return jsonify({'error': 'Error al verificar los datos', 'details': usuarios['error']}), 500
    except OperationalError as e:
        print(f"Error de base de datos: {str(e)}")
        return jsonify({'error': 'Error de base de datos'})
    

    # para crear un usuario nuevo
@my_blueprint.route('/usuarios', methods=['POST'])
def create_user_route():
    from repositories.usuarios_repository import UsuariosRepository
    from app import mysql

    try:
        data = request.get_json()
        nombre = data.get('nombre')
        usuario = data.get('usuario')
        clave = data.get('clave')
        correo = data.get('correo')

        usuarios_repository = UsuariosRepository(mysql.connection)

        result = usuarios_repository.create_user(
            nombre=nombre,
            usuario=usuario,
            clave=clave,
            correo=correo
        )

        if 'success' in result:
            return jsonify({'message': 'Usuario creado exitosamente'}), 201
        else:
            return jsonify({'error': 'Error al crear el usuario', 'details': result['error']}), 500

    except Exception as e:
        print(f"Error al procesar la solicitud: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    # para actualizar la verificacion
@my_blueprint.route('/usuarios/verificar/<string:correo>/<string:nueva_verificacion>', methods=['PUT'])
def update_user_verification_route(correo, nueva_verificacion):
    from repositories.usuarios_repository import UsuariosRepository
    from app import mysql
    
    try:
        usuarios_repository = UsuariosRepository(mysql.connection)
        result = usuarios_repository.update_user_verification(correo, nueva_verificacion)

        if 'success' in result:
            return jsonify(result), 200
        else:
            return jsonify({'error': 'Error al actualizar la verificación', 'details': result['error']}), 500
    except OperationalError as e:
        print(f"Error de base de datos: {str(e)}")
        return jsonify({'error': 'Error de base de datos'})