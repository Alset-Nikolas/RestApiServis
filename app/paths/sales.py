import datetime
from my_logs.logg import info_log
from flask import jsonify, request
from components.schemas.ShopUnit import ShopUnit
from components.schemas.ShopUnitType import ShopUnitType
from sqlalchemy import func
from paths.base_function import response_error_400
from flask import Blueprint

bp_sales = Blueprint('sales', __name__)


def time_valid(time, time_format):
    try:
        datetime.datetime.strptime(time, time_format)
        return True
    except ValueError:
        return False


def get_info(node_id):
    node = ShopUnit.query.filter_by(id=node_id).first()
    info = {
        'id': node.id,
        'name': node.name,
        'date': str(node.date.strftime('%Y-%m-%dT%H:%M:%S.%f%Z')[:-3] + 'Z'),
        'parentId': node.parentId,
        'price': node.price,
        'type': node.type
    }
    return info


def filter_date(time):
    TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
    time = datetime.datetime.strptime(time.isoformat()[:-6], TIME_FORMAT)
    nodes = ShopUnit.query.filter_by(type='OFFER')
    nodes = nodes.filter(ShopUnit.date <= time)
    nodes = nodes.filter(ShopUnit.date >= time - datetime.timedelta(hours=24)).all()
    info_log.info(f'/sales time={time} после фильтра {[(x.name, x.date) for x in nodes]}')
    ans = []
    # nodes = ShopUnit.query.filter(ShopUnit.date.between(time, time - datetime.timedelta(hours=24)))
    for node in nodes:
        ans.append(get_info(node.id))
    return {"items": ans}


@bp_sales.route('/sales', methods=['GET'])
def sales():
    '''
        Получение списка **товаров**, цена которых была обновлена за последние 24 часа включительно [now() - 24h, now()] от
            времени переданном в запросе.
    '''
    info_log.info(f'handler:GET:/sales')
    if 'date' not in request.args:
        info_log.warning(f'/sales Нет параметра date. Аргументы={request.args}, 400')
        return response_error_400()
    time = request.args['date']
    time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    if not time_valid(time=time, time_format=time_format):
        info_log.warning(f'/sales time={time} не валидный формат')
        return response_error_400()
    info_log.info(f'/sales time={time} валидный формат')
    time = datetime.datetime.strptime(time, time_format)
    return jsonify(filter_date(time)), 200
