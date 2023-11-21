from app import mysql
from repositories.consultas_repositoy import ConsultasRepository

consultas_repositoy = ConsultasRepository(mysql.connection)