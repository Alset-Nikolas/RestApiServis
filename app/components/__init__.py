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
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_AS_ASCII'] = False #для кириллицы в конфиге
    db = SQLAlchemy(app)
    migrate = Migrate()
    with app.app_context():
        migrate.init_app(app, db)
    return db





