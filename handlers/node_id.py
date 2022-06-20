import json

from flask import jsonify
from enrollment.db.models import NodeTree
from enrollment import app, db
from enrollment.handlers.base_function import get_info
from enrollment.my_logs.logg import info_log, warning_log



@app.route('/nodes/<id_>', methods=['GET'])
def nodes(id_):
    '''Информация про обьект с id'''
    info_log.info(f'handler:GET:/nodes/<id_>')
    if NodeTree.query.filter_by(node_id=id_).first() is not None:
        info_log.info(f'/nodes/<id_> Информация про обьект с id={id_}, 200')
        return jsonify(get_info(id_)), 200
    warning_log.warning(f'/nodes/<id_>, Нет обьекта с таким id={id_} , 404')
    info_log.warning(f'/nodes/<id_>, Нет обьекта с таким id={id_} , 404')
    return jsonify({
        "code": 404,
        "message": "Item not found"
    }), 404
