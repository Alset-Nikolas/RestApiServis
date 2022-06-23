#!flask/bin/python
import os
import sys
sys.setrecursionlimit(999999)
from flask_migrate import Migrate
from flask import Flask
from app.db import create_app, db


app = create_app()
app.config.from_pyfile('config.py')
app.app_context().push()
from app.paths.delete import bp_delete
from app.paths.imports import bp_imports
from app.paths.node_id import bp_node_id
from app.paths.statistic import bp_statistic
from app.paths.sales import bp_sales

migrate = Migrate()
with app.app_context():
    migrate.init_app(app, db)
#
from app.components.schemas.ShopUnitType import ShopUnitType
from app.components.schemas.ShopUnit import ShopUnit
from app.components.schemas.ShopUnitImport import ShopUnitImport
from app.components.schemas.ShopUnitImportRequest import ShopUnitImportRequest
from app.components.schemas.Error import Error
from app.components.schemas.ShopUnitStatisticUnit import ShopUnitStatisticUnit
from app.consol import bp_consoly


app.register_blueprint(bp_delete)
app.register_blueprint(bp_imports)
app.register_blueprint(bp_node_id)
app.register_blueprint(bp_statistic)
app.register_blueprint(bp_sales)
app.register_blueprint(bp_consoly)

if __name__ == '__main__':
    app.run(debug=True)
    ''', host='0.0.0.0'''















'''
# from flask import Flask, Blueprint
# from app.components import create_app
#
# app = Flask(__name__)
# db = create_app(app)
#
# from app.components.schemas.ShopUnitType import ShopUnitType
# from app.components.schemas.ShopUnit import ShopUnit
# from app.components.schemas.ShopUnitImport import ShopUnitImport
# from app.components.schemas.ShopUnitImportRequest import ShopUnitImportRequest
# from app.components.schemas.Error import Error
# from app.components.schemas.ShopUnitStatisticUnit import ShopUnitStatisticUnit
#
# bp = Blueprint('commands', __name__)
#
#
# @bp.cli.command('create_db')
# def create_db():
#     db.drop_all()
#     db.create_all()
#
#     CATEGORY = ShopUnitType.query.filter_by(type='CATEGORY').first()
#     OFFER = ShopUnitType.query.filter_by(type='OFFER').first()
#
#     if CATEGORY is None:
#         CATEGORY = ShopUnitType(type='CATEGORY')
#         db.session.add(CATEGORY)
#
#     if OFFER is None:
#         OFFER = ShopUnitType(type='OFFER')
#         db.session.add(OFFER)
#
#     db.session.commit()


'''