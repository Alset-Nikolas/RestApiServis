import datetime
from app.my_logs.logg import info_log
from flask import jsonify, request
from app import app, ShopUnitStatisticUnit
from sqlalchemy import func
from app.paths.base_function import response_error_404, response_error_400


def time_valid(time, time_format):
    try:
        datetime.datetime.strptime(time, time_format)
        return True
    except ValueError:
        return False


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


# def save_static_response(info: list):
#     if info:
#         new_line = ShopUnitStatisticResponse()
#         new_line.items = [ShopUnitStatisticUnit.query.filter_by(id=x[0]).filter_by(date=x[1]).first() for x in info]
#         db.session.add(new_line)
#         db.session.commit()

@app.route('/node/<id_>/statistic', methods=['GET'])
def statistic(id_):
    '''
         Получение статистики (истории обновлений) по товару/категории за заданный полуинтервал [from, to).
            Статистика по удаленным элементам недоступна.
    '''
    info_log.info(f'handler:GET:/sales')

    if ShopUnitStatisticUnit.query.filter_by(id=id_).first() is None:
        info_log.warning(f'/node/<id_>/statistic нет id={id_}')
        return response_error_404()

    time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    for data_i in ['dateStart', 'dateEnd']:
        if data_i in request.args:
            time = request.args[f'{data_i}']
            if not time_valid(time=time, time_format=time_format):
                info_log.warning(f'/node/<id_>/statistic {data_i}={time} не валидный формат')
                return response_error_400()

    nodes = ShopUnitStatisticUnit.query.filter_by(id=id_)
    flags = [False, False]
    date_start, date_end = None, None

    if 'dateStart' in request.args:
        flags[0] = True
        date_start = request.args['dateStart']
        nodes = nodes.filter(func.DATE(ShopUnitStatisticUnit.date) >= date_start)
    if 'dateEnd' in request.args:
        flags[1] =True
        date_end = request.args['dateEnd']
        nodes = nodes.filter(func.DATE(ShopUnitStatisticUnit.date) < date_end)
    if all(flags):
        if date_start > date_end:
            info_log.warning(f'/node/<id_>/statistic {data_i}={time} start_time <= end_time ')
            return response_error_400()
    nodes = nodes.all()

    res = []
    save_info_to_static_response = []
    for node_t in nodes:
        t = node_t.date
        type_t = node_t.type.type
        price_t = node_t.price
        ans_i = {
            'date': str(t.strftime('%Y-%m-%dT%H:%M:%S.%f%Z')[:-3] + 'Z'),
            'type': type_t,
            'name': node_t.name,
            'id': node_t.id,
            'parentId': node_t.parentId,
        }
        save_info_to_static_response.append([node_t.id,  t])

        if type_t == 'OFFER':
            ans_i['price'] = price_t
            ans_i['children'] = None
        else:
            summa_, offers = calc_price(id_, t)
            if offers == 0:
                ans_i['price'] = None
            else:
                ans_i['price'] = summa_ // offers
        res.append(ans_i)
    # save_static_response(save_info_to_static_response)
    return jsonify(res), 200
