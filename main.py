#!flask/bin/python
import os
import sys

from app import app, db
sys.setrecursionlimit(999999)
if __name__ == '__main__':
    from app.my_logs.logg import *
    from app.paths.imports import *
    from app.paths.delete import *
    from app.paths.node_id import *
    # from app.paths.sales import *
    info_log.info('1')
    app.run(debug=True)
