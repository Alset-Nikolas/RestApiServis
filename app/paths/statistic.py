import datetime
from app.my_logs.logg import info_log, warning_log
from flask import jsonify, request
from app import app, db, ShopUnit, ShopUnitImport, ShopUnitImportRequest, Error, ShopUnit, ShopUnitType, ShopUnitStatisticUnit
from sqlalchemy import func
from app.paths.base_function import response_error_404, response_error_400


def time_valid(time, time_format):
    try:
        datetime.datetime.strptime(time, time_format)
        return True
    except ValueError:
        return False


# def filter_date(time):
#     nodes = ShopUnit.query.filter(func.DATE(ShopUnit.date) <= time)
#     nodes = nodes.filter(func.DATE(ShopUnit.date) >= time - datetime.timedelta(hours=24))
#     nodes = nodes.filter_by(type=ShopUnitType.query.filter_by(type='OFFER').first())
#
#     info_log.info(f'/sales time={time} после фильтра {[(x.name, x.date) for x in nodes]}')
#     return [get_info({}, node.id)  for node in nodes]


@app.route('/node/<id_>/statistic', methods=['GET'])
def statistic(id_):
    '''Получение списка **товаров**, цена которых была обновлена за последние 24 часа включительно [now() - 24h, now()] от
        времени переданном в запросе.'''
    info_log.info(f'handler:GET:/sales')
    print(id_)
    if ShopUnitStatisticUnit.query.filter_by(id=id_).first() is  None:
        info_log.warning(f'/node/<id_>/statistic нет id={id_}')
        return response_error_404()

    time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    for data_i in ['dateStart', 'dateEnd']:
        if data_i in request.args:
            time= request.args[f'{data_i}']
            if not time_valid(time=time, time_format=time_format):
                info_log.warning(f'/node/<id_>/statistic {data_i}={time} не валидный формат')
                return response_error_400()

    date_start = None
    date_end = None

    if 'dateStart' in request.args:
        date_start = request.args['dateStart']
    if 'dateEnd' in request.args:
        date_end = request.args['dateEnd']
    print('date_start', date_start)
    print('date_end', date_end)
    nodes = ShopUnitStatisticUnit.query.filter_by(id=id_).all()
    print('nodes', nodes)
    times = [(x.date, x.type.type) for x in nodes]

    def calc_price(id, t):
        children = ShopUnitStatisticUnit.query.filter(func.DATE(ShopUnitStatisticUnit.date) < t).filter_by(parentId=id)
        children_id = {x.id for x in children.all()}
        offers = 0
        summa_ = 0
        for ch_id in children_id:
            ch_last = children.filter_by(id=ch_id).order_by(ShopUnitStatisticUnit.date)[-1]
            ch_obj = ShopUnitStatisticUnit.query.filter_by(id=ch_last.id).filter_by(date=ch_last.date).first()
            if ch_obj.type.type == 'OFFER':
                offers += 1
                summa_ += ch_obj.price
            else:
                summa_i, offers = calc_price(id=ch_obj.id, t=t)
        return summa_, offers
    prices = []
    for i, (t, type) in enumerate(times):
        if type == 'OFFER':
            price = nodes[i].price
            prices.append(price)
        else:
            summa_, offers = calc_price(id_, t)
            if offers == 0:
                prices.append(0)
            else:
                prices.append(summa_//offers)





    print('prices', prices)
    return '', 200
    # return jsonify(filter_date(time)), 200
