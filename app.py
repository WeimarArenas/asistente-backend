from flask import Flask, jsonify
from flask_mysqldb import MySQL
from my_blueprint import my_blueprint  # Importa el Blueprint desde my_blueprint.py
from flask_cors import CORS
import base64


app = Flask(__name__)
CORS(app) 

# Configura la base de datos utilizando las credenciales
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '0707MT60FZxSp35*'
app.config['MYSQL_DB'] = 'asistente'

app.register_blueprint(my_blueprint)  # Registra el Blueprint en la aplicación

# Configura la extensión MySQL
mysql = MySQL(app)

if __name__ == '__main__':
    app.run(debug=True)