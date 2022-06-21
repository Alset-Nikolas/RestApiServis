import datetime
from app import app, db, NodeTree
from flask import request, jsonify
from app.my_logs.logg import info_log, warning_log


def valid_request_json(data: dict, time_format: str) -> bool:
    '''Проверка форматы даты и основной структуры'''
    if 'items' not in data or 'updateDate' not in data or len(data) != 2:
        info_log.warning('POST:/imports Проблемы с общей структурой входных данных')
        warning_log.warning(
            f'POST:/imports Проблемы с общей структурой входных данных:\ndata={data}\n, 400')
        return False
    try:
        datetime.datetime.strptime(data['updateDate'], time_format)
        return True
    except ValueError:
        info_log.warning(f'POST:/imports Проблемы с форматом даты')
        warning_log.warning(
            f'POST:/imports Проблемы  с форматом даты:\ndata={data}\n, 400')
        return False


def is_category(node_id: str) -> bool:
    node = NodeTree.query.filter_by(node_id=node_id).first()
    return node.type_ == 'CATEGORY'


def valid_structure_item(item: dict) -> bool:
    if item['type'] in ['CATEGORY', 'OFFER']:
        if all(key in item for key in ['id', 'name', 'type']) and item['name'] is not None:
            return True
    info_log.warning('POST:/imports Проблемы с отдельной структурой item')
    warning_log.warning(
        f'POST:/imports Проблемы с отдельной структурой item:\nitem={item}\n, 400')
    return False


def valid_item(item: dict) -> bool:
    parent_id = value_or_none(dict_=item, key_='parentId')
    price = value_or_zero(dict_=item, key_='price')
    if (parent_id is not None) and (not is_category(parent_id)):
        info_log.warning(f'POST:/imports родителем может быть только категория')
        warning_log.warning(
            f'POST:/imports Проблемы с отдельной структурой item (price) :\nitem={item}\n, 404')
        return False
    if price < 0:
        info_log.warning(f'POST:/imports цена должна быть больше 0')
        warning_log.warning(
            f'POST:/imports Проблемы с отдельной структурой item (price) :\nitem={item}\n, 404')
        return False
    return True


def value_or_none(dict_: dict, key_: str) -> object:
    if key_ in dict_:
        return dict_[key_]
    return None


def value_or_zero(dict_: dict, key_: str) -> int:
    if key_ in dict_:
        return dict_[key_]
    return 0


def add_node(node_id: str, parentId: object, name: str, type_: str, price: int, time_: datetime) -> None:
    new_node = NodeTree(node_id=node_id,
                        parentId=parentId,
                        name=name,
                        type_=type_,
                        price=price,
                        time_=time_,
                        childs=0)
    db.session.add(new_node)
    info_log.info(f'POST:/imports Новый обьект id={node_id}, 200')


def update_parent(node_id: object, diff_price: int, time_update: datetime, diff_child: int) -> None:
    print('update_parent')
    print(node_id, diff_price)
    if node_id is None:
        return
    node = NodeTree.query.filter_by(node_id=node_id).first()
    node.price += diff_price
    node.childs += diff_child
    node.time_ = time_update
    parent_id = node.parentId
    update_parent(node_id=parent_id, diff_price=diff_price, time_update=time_update, diff_child=diff_child)


def update_node(node_id: str, parentId: object, name: str, type_: str, price: int, time_: datetime) -> None:
    node = NodeTree.query.filter_by(node_id=node_id).first()
    node.parentId = parentId
    node.name = name
    node.type_ = type_
    node.price = price
    node.time_ = time_
    info_log.info(
        f'POST:/imports Обновление обьекта id={node_id} name={name}, price={price}, date={time_}, 200')


def id_duplicate(ids: set, new_id: str) -> bool:
    if new_id not in ids:
        ids.add(new_id)
        return False
    info_log.warning(
        f'POST:/imports В 1 запросе не может быть дубликатов id, 400')
    return True


@app.route('/imports', methods=['POST'])
def imports():
    '''Импортирует новые товары и/или категории.'''
    info_log.info('handler:POST:/imports ')

    if not request.is_json:
        return jsonify({"code": 400, "message": "Validation Failed"}), 400

    data = request.get_json()
    time_format = "%Y-%m-%dT%H:%M:%S.%f%z"

    if not valid_request_json(data, time_format):
        return jsonify({"code": 400, "message": "Validation Failed"}), 400

    update_date = datetime.datetime.strptime(data['updateDate'], time_format)
    ids = set()
    for item in data['items']:
        if not valid_structure_item(item) or not valid_item(item) or id_duplicate(ids, item['id']):
            db.session.rollback()
            return jsonify({"code": 400, "message": "Validation Failed"}), 400
        new_parent_id = value_or_none(dict_=item, key_='parentId')
        price = value_or_zero(dict_=item, key_='price')
        node = NodeTree.query.filter_by(node_id=item['id']).first()

        if node is not None:
            print(node.node_id, node.parentId)
            old_price = node.price
            old_parent_id = node.parentId
            print('old_parent_id', old_parent_id)
            update_node(
                node_id=item['id'],
                parentId=new_parent_id,
                name=item['name'],
                type_=item['type'],
                price=price,
                time_=update_date
            )
        else:
            old_price = 0
            old_parent_id = None

            add_node(
                node_id=item['id'],
                parentId=new_parent_id,
                name=item['name'],
                type_=item['type'],
                price=price,
                time_=update_date
            )
        diff_child = int(item['type'] == 'OFFER')

        if old_parent_id is None :
            update_parent(new_parent_id, diff_price=price, time_update=update_date, diff_child=diff_child)
        elif old_parent_id == new_parent_id:
            update_parent(new_parent_id, diff_price=price - old_price, time_update=update_date, diff_child=0)
        else:
            update_parent(old_parent_id, diff_price=-old_price, time_update=update_date,
                          diff_child=-diff_child)
            update_parent(new_parent_id, diff_price=price, time_update=update_date,
                          diff_child=diff_child)


    db.session.commit()
    return '', 200
