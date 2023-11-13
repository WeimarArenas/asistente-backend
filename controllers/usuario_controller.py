from app import mysql
from repositories.usuarios_repository import UsuariosRepository

usuarios_repository = UsuariosRepository(mysql.connection)