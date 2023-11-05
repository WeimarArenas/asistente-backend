from app import mysql
from repositories.evento_repository import EventosRepository

eventos_repository = EventosRepository(mysql.connection)