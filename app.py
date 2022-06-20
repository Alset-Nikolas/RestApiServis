#!flask/bin/python
import os

from yandex_rest_api_server.ServisRestApi.enrollment import absolute_path, db, app



if __name__ == '__main__':
    from enrollment.my_logs.logg import info_log
    from handlers.node_id import *
    from handlers.imports import *
    from handlers.delete import *
    from handlers.sales import *

    if not os.path.exists(absolute_path):
        info_log.info(f'Создание таблицы path={absolute_path}')
        db.create_all()
    app.run(debug=True)
