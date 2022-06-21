#!flask/bin/python
import os
import sys

from app import app, absolute_path, db
sys.setrecursionlimit(999999)
if __name__ == '__main__':
    from app.my_logs.logg import info_log
    from app.handlers.imports import *
    from app.handlers.delete import *
    from app.handlers.node_id import *
    from app.handlers.sales import *
    app.run(debug=True)
