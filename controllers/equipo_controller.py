from app import mysql  # Importa la instancia de MySQL desde app.py
from repositories.equipo_repository import EquipoRepository

equipo_repository = EquipoRepository(mysql.connection)
