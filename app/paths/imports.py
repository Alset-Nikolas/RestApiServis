import datetime
from app import app, db, ShopUnit, ShopUnitImport, ShopUnitImportRequest, Error, ShopUnit, ShopUnitType
from flask import request, jsonify
from app.my_logs.logg import info_log, warning_log
from .base_function import delete_child

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
        print(price)
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
        if parent.children is not None:
            parent.children = set(list(parent.children) + [id_child])
        else:
            parent.children = [id_child]



def check_type_context(type, price):
    if type == 'CATEGORY':
        if price is not None:
            info_log.warning(
                f'POST:/imports В 1 запросе не может быть дубликатов type={type} price!={price}, 400', )
            return False
    if type == 'OFFER':
        if price is None or price < 0:
            info_log.warning(
                f'POST:/imports В 1 запросе не может быть дубликатов type={type} price!={price}, 400', )
            return False

    return True


def add_node(node_id: str, parentId: object, name: str, type_: str, price: object, time_: datetime) -> None:
    new_node = ShopUnit(id=node_id, name=name, date=time_, type=type_)
    new_node.parentId = parentId
    add_child(id_child=node_id, id_parent=parentId)
    new_node.price = price
    db.session.add(new_node)

    save_import_fact(node_id, name, parentId, type_, price)
    info_log.info(f'POST:/imports Новый обьект id={node_id}, 200')


def update_parent(node_id: object, time_update: datetime) -> None:
    if node_id is None:
        return
    node = ShopUnit.query.filter_by(id=node_id).first()
    node.date = time_update
    db.session.add(node)
    update_parent(node_id=node.parentId,time_update=time_update)

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


def update_node(node_id: str, old_parentId, parentId: object, name: str, type_: str, price: object, time_: datetime) -> None:
    node = ShopUnit.query.filter_by(id=node_id).first()
    node.parentId = parentId
    delete_child(id_child=node_id, id_parent=old_parentId)
    add_child(id_child=node_id, id_parent=parentId)
    node.name = name
    node.type = type_
    node.price = price
    node.date = time_
    db.session.add(node)

    save_import_fact(node_id, name, parentId, type_, price)

    info_log.info(
        f'POST:/imports Обновление обьекта id={node_id} name={name}, price={price}, date={time_}, 200')


def id_duplicate(ids: set, new_id: str) -> bool:
    if new_id not in ids:
        ids.add(new_id)
        return False
    info_log.warning(
        f'POST:/imports В 1 запросе не может быть дубликатов id={ids} + {new_id}, 400',)
    return True


def response_error():
    db.session.rollback()
    db.session.add(Error(code=400, message='Validation Failed'))
    db.session.commit()
    return jsonify({"code": 400, "message": "Validation Failed"}), 400


@app.route('/imports', methods=['POST'])
def imports():
    '''Импортирует новые товары и/или категории.'''
    info_log.info('handler:POST:/imports ')

    if not request.is_json:
        return response_error()

    data = request.get_json()
    time_format = "%Y-%m-%dT%H:%M:%S.%f%z"

    if not valid_request_json(data, time_format):
        return response_error()

    update_date = datetime.datetime.strptime(data['updateDate'], time_format)
    update_date = update_date.isoformat()
    ids = set()
    for item in data['items']:
        print("not valid_structure_item(item) or not valid_item(item) or id_duplicate(ids, item['id'])", not valid_structure_item(item) ,
              not valid_item(item) , id_duplicate(ids, item['id']))
        if (not valid_structure_item(item)) or (not valid_item(item)) or (not id_duplicate(ids, item['id'])):
            return response_error()
        new_parent_id = value_or_none(dict_=item, key_='parentId')
        price = value_or_none(dict_=item, key_='price')
        node = ShopUnit.query.filter_by(id=item['id']).first()
        type_obj = ShopUnitType.query.filter_by(type=item['type']).first()
        print(not check_type_context(type_obj.type, price))
        if not check_type_context(type_obj.type, price):
            return response_error()
        old_parent_id = None
        if node is not None:
            print(node.name, update_date)
            old_parent_id = node.parentId
            update_node(
                node_id=item['id'],
                parentId=new_parent_id,
                name=item['name'],
                type_=type_obj,
                price=price,
                time_=update_date,
                old_parentId=old_parent_id,
            )
        else:
            print('new', update_date, item['name'])

            add_node(
                node_id=item['id'],
                parentId=new_parent_id,
                name=item['name'],
                type_=type_obj,
                price=price,
                time_=update_date
            )

        if new_parent_id is not None :
            update_parent(new_parent_id,time_update=update_date)
        # if old_parent_id is not None:
        #     update_parent(old_parent_id, time_update=update_date)


    save_request_fact(ids, update_date)

    db.session.commit()
    return '', 200
