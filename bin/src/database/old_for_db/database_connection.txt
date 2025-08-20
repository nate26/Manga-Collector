'''DB connection with configurations to setup the DB'''
import json
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

f = open('database/database_conf.json', 'r', encoding='UTF-8')
data = json.load(f)
conf = {
    'endpoint': data.get('endpoint'),
    'port': '5432',
    'name': 'postgres',
    'user': data.get('user'),
    'password': data.get('password')
}
f.close()

app.config['SQLALCHEMY_DATABASE_URI'] \
    = 'postgresql://{user}:{password}@{endpoint}:{port}/{name}'.format(**conf)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
