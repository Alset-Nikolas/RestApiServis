print('app.component.__init__')
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

def create_app(app):
    DATABASE = {
        'drivername': 'postgresql',
        'host': 'localhost',
        'port': '5432',
        'username': 'postgres',
        'password': 'qwerty',
        'database': 'probe.db'
    }
    db_url = f'postgresql+psycopg2://{DATABASE["username"]}:{DATABASE["password"]}@{DATABASE["host"]}/{DATABASE["database"]}'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db = SQLAlchemy(app)
    migrate = Migrate()
    with app.app_context():
        migrate.init_app(app, db)
    return db

# from .schemas.ShopUnitType import *
# from .schemas.ShopUnit import *
# from .schemas.ShopUnitImport import *
# from .schemas.ShopUnitImportRequest import *
# from .schemas.Error import *




