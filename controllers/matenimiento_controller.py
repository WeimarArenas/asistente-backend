from app import mysql
from repositories.mantenimiento_repository import MantenimientosRepository

mantenimientos_repository = MantenimientosRepository(mysql.connection)