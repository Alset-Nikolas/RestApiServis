import os
DATABASE = {
    'drivername': 'postgresql',
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',
    'password': 'qwerty',
    'database': 'probe.db'
}

db_url = f'postgresql+psycopg2://{DATABASE["username"]}:{DATABASE["password"]}@{DATABASE["host"]}/{DATABASE["database"]}'
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', db_url)
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSON_AS_ASCII = False  # для кириллицы в конфиге