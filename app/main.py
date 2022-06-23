#!flask/bin/python
import sys
from flask_migrate import Migrate
from app.db import create_app, db
from app.paths.delete import bp_delete
from app.paths.imports import bp_imports
from app.paths.node_id import bp_node_id
from app.paths.statistic import bp_statistic
from app.paths.sales import bp_sales
from app.consol import bp_consoly

from app.components import bp_postgres
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
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
