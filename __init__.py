from flask_sqlalchemy import SQLAlchemy
from flask import Flask



app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
absolute_path = 'tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{absolute_path}'
db = SQLAlchemy(app)