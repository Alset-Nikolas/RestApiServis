from flask import jsonify
from flask import Blueprint
from app.db import db
from app.components.schemas.ShopUnit import ShopUnit
from app.my_logs.logg import info_log, warning_log
from .base_function import response_error_404, response_error_400, delete_child
bp_delete = Blueprint('delete', __name__)

def delete_one_node(node_id: int) -> None:
    '''
        Удалить узел по id
    '''
    node = ShopUnit.query.filter_by(id=node_id).first()
    info_log.info(f'/delete/<id_>  Удаляем id={node_id}. name="{node.name}"')
    db.session.delete(node)


def recursively_delete_nodes(node_id: int) -> None:
    '''
        Рекурсивно удалить детей узла из таблицы
    '''
    node_del = ShopUnit.query.filter_by(id=node_id).first()
    children = node_del.children
    info_log.info(f'/delete/<id_> Рекурсивно удаляем id={node_id}. детей={children}')
    if children is None:
        delete_one_node(node_id)
        return
    for child_id in children:
        recursively_delete_nodes(child_id)
    delete_one_node(node_id)


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
    delete_child(id_child=id_, id_parent=node_del.parentId)
    recursively_delete_nodes(id_)
    db.session.commit()
    return '', 200
