#!flask/bin/python
import sys
from flask_migrate import Migrate
from db import create_app, db
from paths.delete import bp_delete
from paths.imports import bp_imports
from paths.node_id import bp_node_id
from paths.statistic import bp_statistic
from paths.sales import bp_sales
from components import bp_postgres
from consol import bp_consoly


app = create_app()
app.app_context().push()
migrate = Migrate()
with app.app_context():
    migrate.init_app(app, db)


app.register_blueprint(bp_postgres)
app.register_blueprint(bp_delete)
app.register_blueprint(bp_imports)
app.register_blueprint(bp_node_id)
app.register_blueprint(bp_statistic)
app.register_blueprint(bp_sales)
app.register_blueprint(bp_consoly)

sys.setrecursionlimit(999999)

from my_logs.logg import info_log, warning_log



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

'''
export FLASK_APP=app/main
flask db init
'''