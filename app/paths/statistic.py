import datetime
from my_logs.logg import info_log
from flask import jsonify, request
from components.schemas.ShopUnitStatistic import ShopUnitStatistic
from sqlalchemy import func
from paths.base_function import response_error_404, response_error_400
from flask import Blueprint
from sqlalchemy import desc

bp_statistic = Blueprint('statistic', __name__)
time_format = "%Y-%m-%dT%H:%M:%S.%f%z"


def time_valid(time, time_format):
    try:
        datetime.datetime.strptime(time, time_format)
        return True
    except ValueError:
        return False


def calc_price(ans, id, t):
    node = ShopUnitStatistic.query.filter_by(id=id).filter_by(date=t).first()
    ans['date'] = str(node.date.strftime(time_format))[:-3] + 'Z'
    ans['type'] = node.type
    ans['name'] = node.name
    ans['id'] = id
    ans['parentId'] = node.parentId
    # ans['children'] = []

    children = ShopUnitStatistic.query.filter(func.DATE(ShopUnitStatistic.date) < t)
    children = children.filter_by(parentId=id)
    children_id = {x.id for x in children.all()}
    offers = 0
    summa_ = 0
    for ch_id in children_id:
        children = children.filter_by(id=ch_id)
        ch_last = children.order_by(desc(ShopUnitStatistic.date)).first()
        if ch_last is not None:
            ans_ch, summa_i, offers_i = calc_price(ans={}, id=ch_last.id, t=ch_last.date)
            # ans['children'].append(ans_ch)
            summa_ += summa_i
            offers += offers_i
    if node.type == 'OFFER':
        offers += 1
        summa_ += node.price

    if offers == 0:
        ans['price'] = None
    else:
        ans['price'] = summa_ // offers
    # input()
    return ans, summa_, offers


# def save_static_response(info: list):
#     if info:
#         new_line = ShopUnitStatisticResponse()
#         new_line.items = [ShopUnitStatisticUnit.query.filter_by(id=x[0]).filter_by(date=x[1]).first() for x in info]
#         db.session.add(new_line)
#         db.session.commit()

@bp_statistic.route('/node/<id_>/statistic', methods=['GET'])
def statistic(id_):
    '''
         Получение статистики (истории обновлений) по товару/категории за заданный полуинтервал [from, to).
            Статистика по удаленным элементам недоступна.
    '''
    info_log.info(f'handler:GET:/sales')

    if ShopUnitStatistic.query.filter_by(id=id_).first() is None:
        info_log.warning(f'/node/<id_>/statistic нет id={id_}')
        return response_error_404()

    time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    for data_i in ['dateStart', 'dateEnd']:
        if data_i in request.args:
            time = request.args[f'{data_i}']
            if not time_valid(time=time, time_format=time_format):
                info_log.warning(f'/node/<id_>/statistic {data_i}={time} не валидный формат')
                return response_error_400()

    nodes = ShopUnitStatistic.query.filter_by(id=id_)
    flags = [False, False]
    date_start, date_end = None, None
    if 'dateStart' in request.args:
        flags[0] = True
        date_start = request.args['dateStart']
        nodes = nodes.filter(ShopUnitStatistic.date >= date_start)
        print(nodes.all())

    if 'dateEnd' in request.args:
        flags[1] = True
        date_end = request.args['dateEnd']
        nodes = nodes.filter(ShopUnitStatistic.date < date_end)

    if all(flags):
        if date_start > date_end:
            info_log.warning(f'/node/<id_>/statistic start_time <= end_time  {date_start} <=! {date_end}')
            return response_error_400()
    nodes = nodes.all()
    res = []
    save_info_to_static_response = []
    for node_t in nodes:
        t = node_t.date
        save_info_to_static_response.append([node_t.id, t])
        ans_i, summa_, offers = calc_price({}, id_, t)
        res.append(ans_i)
    # save_static_response(save_info_to_static_response)
    ans = {'items':res}
    return jsonify(ans), 200
