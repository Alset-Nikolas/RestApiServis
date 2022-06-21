from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
absolute_path = basedir
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)


from app.components.schemas.ShopUnitType import *