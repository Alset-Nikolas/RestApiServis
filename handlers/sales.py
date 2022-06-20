import datetime
from enrollment.my_logs.logg import info_log, warning_log
from flask import jsonify, request
from enrollment import app
from enrollment.db.models import NodeTree
from sqlalchemy import func
from enrollment.handlers.base_function import get_info

def time_valid(time, time_format):
    try:
        datetime.datetime.strptime(time, time_format)
        return True
    except ValueError:
        return False

def filter_date(time):
    nodes = NodeTree.query.filter(func.DATE(NodeTree.time_) <= time).filter(func.DATE(NodeTree.time_) >= time- datetime.timedelta(hours=24)).filter_by(type_='OFFER')
    info_log.info(f'/sales time={time} после фильтра {[(x.name, x.time_) for x in nodes]}')
    return [get_info(node.node_id) for node in nodes]

@app.route('/sales', methods=['GET'])
def sales():
    '''Получение списка **товаров**, цена которых была обновлена за последние 24 часа включительно [now() - 24h, now()] от
        времени переданном в запросе.'''

    '''
    http://127.0.0.1:5000/sales?date=2022-02-04T00%3A00%3A00.000Z
    '''

    info_log.info(f'handler:GET:/sales')
    if 'date' not in request.args:
        info_log.warning(f'/sales Нет параметра date. Аргументы={request.args}, 400')
        return jsonify({
                      "code": 400,
                      "message": "Validation Failed"
                    }), 400
    time = request.args['date']
    time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    if not time_valid(time=time, time_format = time_format):
        info_log.warning(f'/sales time={time} не валидный формат')
        return jsonify({
            "code": 400,
            "message": "Validation Failed"
        }), 400
    info_log.info(f'/sales time={time} валидный формат')
    time = datetime.datetime.strptime(time, time_format)
    return jsonify(filter_date(time)), 200
