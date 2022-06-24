import datetime
from my_logs.logg import info_log
from flask import jsonify, request
from components.schemas.ShopUnit import ShopUnit
from components.schemas.ShopUnitType import ShopUnitType
from sqlalchemy import func
from paths.base_function import response_error_400
from .node_id import get_info
from flask import Blueprint

bp_sales = Blueprint('sales', __name__)


def time_valid(time, time_format):
    try:
        datetime.datetime.strptime(time, time_format)
        return True
    except ValueError:
        return False


def filter_date(time):
    nodes = ShopUnit.query.filter(func.DATE(ShopUnit.date) <= time)
    nodes = nodes.filter(func.DATE(ShopUnit.date) >= time - datetime.timedelta(hours=24))
    nodes = nodes.filter_by(type='OFFER')

    info_log.info(f'/sales time={time} после фильтра {[(x.name, x.date) for x in nodes]}')
    return [get_info({}, node.id) for node in nodes]


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
