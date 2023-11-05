from app import mysql
from repositories.calibracion_repository import CalibracionesRepository

calibracion_repository = CalibracionesRepository(mysql.connection)

