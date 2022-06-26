import datetime
from sqlalchemy import func
from flask import jsonify
from flask import Blueprint
from db import db
from components.schemas.ShopUnit import ShopUnit
from components.schemas.ShopUnitStatistic import ShopUnitStatistic
from my_logs.logg import info_log
from .base_function import response_error_404, response_error_400, delete_child

bp_delete = Blueprint('delete', __name__)


def delete_one_node(node_id: int) -> None:
    '''
        Удалить узел по id из таблицы ShopUnit
    '''


    node = ShopUnit.query.filter_by(id=node_id).first()
    info_log.info(f'/delete/<id_>  Удаляем id={node_id}. name="{node.name}"')
    date_create = node.date
    recursively_delete_statistic(node_id, date_create)
    db.session.delete(node)



def delete_statistic(node_id, date_create):
    '''
         Удалить узлы по id из таблицы ShopUnitStatistic
     '''
    for node_stat in ShopUnitStatistic.query.filter_by(id=node_id).filter(func.DATE(ShopUnitStatistic.date) <= date_create).all():
        db.session.delete(node_stat)

def recursively_delete_nodes(node_id: int) -> None:
    '''
        Рекурсивно удалить детей узла из таблицы
    '''
    node_del = ShopUnit.query.filter_by(id=node_id).first()
    children = node_del.children
    info_log.info(f'/delete/<id_> Рекурсивно удаляем id={node_id}. детей={children}')
    if children is None:
        # если type == offer -> children is None
        delete_one_node(node_id)
        return
    for child_id in children:
        recursively_delete_nodes(child_id)
    delete_one_node(node_id)

def recursively_delete_statistic(node_id: int, date_create:datetime) -> None:
    '''
        Рекурсивно удалить детей узла из таблицы ShopUnitStatistic
    '''
    if node_id is None:
        return
    children = ShopUnitStatistic.query.filter_by(parentId=node_id).filter(func.DATE(ShopUnitStatistic.date) <= date_create).all()
    info_log.info(f'/delete/<id_> Рекурсивно stat удаляем id={node_id}. детей={children}')
    if children is None:
        # если type == offer -> children is None
        delete_statistic(node_id, date_create)
        return
    for child_id in [x.id for x in children]:
        recursively_delete_statistic(child_id, date_create)
    delete_statistic(node_id, date_create)

def valid_id(id_: int) -> bool:
    '''
        Проверка на валидность id узла
    '''
    return isinstance(id_, str) and id_ != '' and id_ != 'None' and (id_ is not None) and id_ != 'null'


@bp_delete.route('/delete/<id_>', methods=['DELETE'])
def delete(id_):
    '''
        Обработчик удаление элемента по идентификатору.
        При удалении категории удаляются все дочерние элементы.
     '''
    if not valid_id(id_):
        info_log.warning(f'/delete/<id_> не валидный id={id_}, 400')
        return response_error_400()

    node_del = ShopUnit.query.filter_by(id=id_).first()

    if node_del is None:
        info_log.warning(f'/delete/<id_> нет в бд id={id_}, 404')
        return response_error_404()

    info_log.info(f'handler:DELETE:/delete/<id_> id_={id_} name="{node_del.name}"')
    delete_child(id_child=id_, id_parent=node_del.parentId) # удаляем ссылку у родителя
    recursively_delete_nodes(id_)
    db.session.commit()
    return '', 200
