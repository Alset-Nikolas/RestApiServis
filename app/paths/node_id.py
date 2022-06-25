from flask import jsonify
from components.schemas.ShopUnit import ShopUnit
from .base_function import response_error_404
from my_logs.logg import info_log, warning_log
from flask import Blueprint

bp_node_id = Blueprint('node_id', __name__)


def get_info(ans, id_node: str) -> tuple:
    '''Вернуть ниформацию о узле и его детей'''
    node = ShopUnit.query.filter_by(id=id_node).first()
    type = node.type

    ans["type"] = type
    ans["name"] = node.name
    ans["id"] = node.id
    ans["parentId"] = node.parentId
    ans["date"] = str(node.date.strftime('%Y-%m-%dT%H:%M:%S.%f%Z')[:-3] + 'Z')
    ans['children'] = []
    sum_price = 0
    offers = 0
    childs = node.children
    if childs is None:
        #т.е это offer
        ans['children'] = None
        ans['price'] = node.price
        return ans, node.price, 1
    if len(childs) == 0:
        #пустая категория
        ans['children'] = []
        ans['price'] = None
        return ans, 0, 0

    for child_id in childs:
        ans_i = dict()
        ans_i, sum_i, offers_i = get_info(ans_i, child_id)
        ans['children'].append(ans_i)
        sum_price += sum_i
        offers += offers_i

    if offers == 0:
        ans["price"] = None
    else:
        ans["price"] = sum_price // offers

    return ans, sum_price, offers


@bp_node_id.route('/nodes/<id_>', methods=['GET'])
def nodes(id_):
    '''
        Обработчик по выводу информации по id
    '''
    info_log.info(f'handler:GET:/nodes/<id_>')
    if ShopUnit.query.filter_by(id=id_).first() is not None:
        info_log.info(f'/nodes/<id_> Информация про обьект с id={id_}, 200')
        ans = dict()
        ans, _, _ = get_info(ans, id_)
        return jsonify(ans), 200
    warning_log.warning(f'/nodes/<id_>, Нет обьекта с таким id={id_} , 404')
    info_log.warning(f'/nodes/<id_>, Нет обьекта с таким id={id_} , 404')
    return response_error_404()
