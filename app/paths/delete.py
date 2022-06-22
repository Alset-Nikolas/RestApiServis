from flask import jsonify
from app import app, db, NodeTree
from app.my_logs.logg import info_log, warning_log


def delete_one_node(node_id: int) -> None:
    '''
        Удалить узел по id
    '''
    node = NodeTree.query.filter_by(node_id=node_id).first()
    info_log.info(f'/delete/<id_>  Удаляем id={node_id}. name="{node.name}"')
    db.session.delete(node)
    db.session.commit()


def recursively_delete_nodes(node_id: int) -> None:
    '''
        Рекурсивно удалить детей узла из таблицы
    '''
    childs = NodeTree.query.filter_by(parentId=node_id).all()
    info_log.info(f'/delete/<id_> Рекурсивно удаляем id={node_id}. детей={len(childs)}')
    if childs == []:
        delete_one_node(node_id)
        return
    for child in childs:
        child_id = child.node_id
        recursively_delete_nodes(child_id)
    delete_one_node(node_id)


def valid_id(id_: int) -> bool:
    '''
        Проверка на валидность id узла
    '''
    return isinstance(id_, str) and id_ != '' and id_ != 'None' and (id_ is not None) and id_ != 'null'


def update_parent(parent_id: int, node_del: int) -> None:
    '''
        Обновление цены(price) и кол-ва детей(childs) у предков
    '''
    while parent_id is not None:
        parent = NodeTree.query.filter_by(node_id=parent_id).first()
        info_log.info(
            f'/delete/<id_> Родитель: id={parent_id} name="{parent.name}". ДО удаления: кол-во детей={parent.childs}, денег={parent.price}')
        if node_del.type_ == 'OFFER':
            parent.childs -= 1
        else:
            parent.childs -= node_del.childs
        parent.price -= node_del.price
        info_log.info(
            f'/delete/<id_> Родитель: id={parent_id} name="{parent.name}". ПОСЛЕ удаления: кол-во детей={parent.childs}, денег={parent.price}')

        parent_id = parent.parentId
        db.session.commit()

    else:
        info_log.info(
            f'/delete/<id_> Родитель: id={None}')


@app.route('/delete/<id_>', methods=['DELETE'])
def delete(id_):
    '''
        Обработчик удаление элемента по идентификатору.
        При удалении категории удаляются все дочерние элементы.
     '''

    if not valid_id(id_):
        return jsonify({"code": 400, "message": "Validation Failed"}), 400

    node_del = NodeTree.query.filter_by(node_id=id_).first()

    if node_del is None:
        info_log.warning(f'/delete/<id_> нет в бд id={id_}, 404')
        return jsonify({"code": 404, "message": "Item not found"}), 404

    info_log.info(f'handler:DELETE:/delete/<id_> id_={id_} name="{node_del.name}"')
    update_parent(parent_id=node_del.parentId, node_del=node_del)
    recursively_delete_nodes(id_)
    return '', 200
