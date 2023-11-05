from app import mysql
from repositories.areas_repository import AreaRepository

area_repository = AreaRepository(mysql.connection)