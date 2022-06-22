import datetime
from app import app, db, ShopUnit, ShopUnitImport, ShopUnitImportRequest, Error, ShopUnit, ShopUnitType
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


def is_category(node_id: object) -> bool:
    if node_id is None:
        return True
    node = ShopUnit.query.filter_by(id=node_id).first()
    category_obj = node.type
    return category_obj.type == 'CATEGORY'


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
    price = value_or_none(dict_=item, key_='price')
    if not is_category(parent_id):
        info_log.warning(f'POST:/imports родителем может быть только категория')
        warning_log.warning(
            f'POST:/imports Проблемы с отдельной структурой item (price) :\nitem={item}\n, 404')
        return False
    if price is not None and price < 0:
        info_log.warning(f'POST:/imports цена должна быть больше 0')
        warning_log.warning(
            f'POST:/imports Проблемы с отдельной структурой item (price) :\nitem={item}\n, 404')
        return False
    return True


def value_or_none(dict_: dict, key_: str) -> object:
    if key_ in dict_:
        return dict_[key_]
    return None

def add_child(id_child, id_parent):
    parent = ShopUnit.query.filter_by(id=id_parent).first()
    if parent:
        new_child = ShopUnit.query.filter_by(id=id_child).first()

        if parent.children is not None:
            parent.children = list(parent.children) +[new_child.id]
        else:
            parent.children = [new_child.id]

def check_type_context(type, price):
    if type=='CATEGORY':
        if price is not None:
            return False
    if type == 'OFFER':
        if price is None or price < 0:
            return False
    return True





def add_node(node_id: str, parentId: object, name: str, type_: str, price: object, time_: datetime) -> None:
    new_node = ShopUnit(id=node_id,name=name,date=time_,type=type_)
    new_node.parentId = parentId
    add_child(id_child=node_id, id_parent=parentId)
    new_node.price = price
    db.session.add(new_node)

    save_import_fact(node_id, name, parentId, type_, price)

    info_log.info(f'POST:/imports Новый обьект id={node_id}, 200')


def update_parent(node_id: object, diff_price: int, time_update: datetime, diff_child: int) -> None:

    if node_id is None:
        return
    node = ShopUnit.query.filter_by(id=node_id).first()
    # node.price += diff_price
    # node.childs += diff_child
    node.time_ = time_update
    parent_id = node.parentId
    update_parent(node_id=parent_id, diff_price=diff_price, time_update=time_update, diff_child=diff_child)

def save_import_fact(node_id, name, parentId, type, price):
    unit_import = ShopUnitImport.query.filter_by(id=node_id).first()
    if unit_import is None:
        unit_import = ShopUnitImport(id=node_id, name=name, type=type)

    unit_import.name = name
    unit_import.parentId = parentId
    unit_import.type = type
    unit_import.price = price
    db.session.add(unit_import)

def save_request_fact(ids, update_date):
    new_import_request = ShopUnitImportRequest()
    new_import_request.items = list(ids)
    new_import_request.updateDate = update_date
    db.session.add(new_import_request)

def update_node(node_id: str, parentId: object, name: str, type_: str, price: object, time_: datetime) -> None:
    node = ShopUnit.query.filter_by(id=node_id).first()
    node.parentId = parentId
    add_child(id_child=node_id, id_parent=parentId)
    node.name = name
    node.type = type_
    node.price = price
    node.data = time_
    db.session.add(node)

    save_import_fact(node_id, name, parentId, type_, price)

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
        price = value_or_none(dict_=item, key_='price')
        node = ShopUnit.query.filter_by(id=item['id']).first()
        type_obj = ShopUnitType.query.filter_by(type=item['type']).first()

        if not check_type_context(type_obj.type, price):
            db.session.rollback()
            return jsonify({"code": 400, "message": "Validation Failed"}), 400

        if node is not None:
            old_price = node.price
            old_parent_id = node.parentId
            update_node(
                node_id=item['id'],
                parentId=new_parent_id,
                name=item['name'],
                type_=type_obj,
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
                type_=type_obj,
                price=price,
                time_=update_date
            )
        # diff_child = int(item['type'] == 'OFFER')

        # if old_parent_id is None :
        #     update_parent(new_parent_id, diff_price=price, time_update=update_date, diff_child=diff_child)
        # elif old_parent_id == new_parent_id:
        #     update_parent(new_parent_id, diff_price=price - old_price, time_update=update_date, diff_child=0)
        # else:
        #     update_parent(old_parent_id, diff_price=-old_price, time_update=update_date,
        #                   diff_child=-diff_child)
        #     update_parent(new_parent_id, diff_price=price, time_update=update_date,
        #                   diff_child=diff_child)
    #
    save_request_fact(ids, update_date)

    db.session.commit()
    return '', 200
