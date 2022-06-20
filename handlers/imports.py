import datetime
from enrollment.db.models import NodeTree
from enrollment import app, db
from flask import request, jsonify
from enrollment.my_logs.logg import info_log, warning_log

def valid_request_json(data, time_format):
    if 'items' not in data or 'updateDate' not in data or len(data) != 2:
        return False
    try:
        datetime.datetime.strptime(data['updateDate'], time_format)
        return True
    except ValueError:
        return False

def is_category(node_id):
    node = NodeTree.query.filter_by(node_id=node_id).first()
    return node.type_ == 'CATEGORY'

def valid_request_item(item):
    if item['type'] in ['CATEGORY', 'OFFER']:
        return all(key in item for key in ['id', 'name', 'type']) and item['name'] is not None
    return False

def check_key_difference(items):
    ids = set()
    for item in items:
        if 'id' in item:
            ids.add(item['id'])
        else:
            return False
    return len(ids) == len(items)



def value_or_none(dict_, key_):
    if key_ in dict_:
        return dict_[key_]
    return None


def value_or_zero(dict_, key_):
    if key_ in dict_:
        return dict_[key_]
    return 0


def add_node(node_id, parentId, name, type_, price, time_):
    new_node = NodeTree(node_id=node_id,
                        parentId=parentId,
                        name=name,
                        type_=type_,
                        price=price,
                        time_=time_,
                        childs=0)
    db.session.add(new_node)
    db.session.commit()


def go_up(node_id, delta, time_update, flag_):
    if node_id is None:
        return
    node = NodeTree.query.filter_by(node_id=node_id).all()[0]

    if node.price is None:
        node.price = 0
    node.price += delta
    if flag_:
        node.childs += 1
    node.time_ = time_update
    parent_id = node.parentId
    db.session.commit()
    go_up(node_id=parent_id, delta=delta, time_update=time_update, flag_=flag_)


def update_node(node_id, parentId, name, type_, price, time_):
    node = NodeTree.query.filter_by(node_id=node_id).first()
    node.parentId = parentId
    node.name = name
    node.type_ = type_
    node.price = price
    node.time_ = time_
    db.session.commit()



@app.route('/imports', methods=['POST'])
def imports():
    '''Импортирует новые товары и/или категории.'''
    info_log.info('handler:POST:/imports ')
    json_error_import = jsonify({
        "code": 400,
        "message": "Validation Failed"
    })


    if not request.is_json:
        return json_error_import, 400
    data = request.get_json()
    time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    if not valid_request_json(data, time_format) and check_key_difference(data['items']):
        info_log.warning('POST:/imports Проблемы с общей структурой входных данных')
        warning_log.warning(f'POST:/imports Проблемы с общей структурой входных данных:\ndata={data}\n time_format={time_format}, 404')
        return json_error_import, 400
    update_date = datetime.datetime.strptime(data['updateDate'], time_format)
    for item in data['items']:
        if valid_request_item(item):
            parent_id = value_or_none(dict_=item, key_='parentId')
            price = value_or_zero(dict_=item, key_='price')
            if (parent_id is not None) and (not is_category(parent_id)):
                info_log.warning(f'POST:/imports родитем может быть только категория  parent_id={parent_id}')
                warning_log.warning(
                    f'POST:/imports Проблемы с отдельной структурой item (price) :\nitem={item}\n, 404')
                return json_error_import, 400
            if price <0:
                info_log.warning(f'POST:/imports цена должна быть больше 0,  price={price}')
                warning_log.warning(
                    f'POST:/imports Проблемы с отдельной структурой item (price) :\nitem={item}\n, 404')
                return json_error_import, 400
            if NodeTree.query.filter_by(node_id=item['id']).first() is not None:
                old_price = NodeTree.query.filter_by(node_id=item['id']).first().price

                update_node(
                    node_id=item['id'],
                    parentId=parent_id,
                    name=item['name'],
                    type_=item['type'],
                    price=price,
                    time_=update_date
                )
                info_log.info(f'POST:/imports Обновление обьекта id={item["id"]} name={item["name"]}, price={price}, date={update_date}, 200')
                if parent_id is not None:
                    go_up(parent_id, delta=price-old_price, time_update=update_date, flag_= False)
            else:
                add_node(
                    node_id=item['id'],
                    parentId=parent_id,
                    name=item['name'],
                    type_=item['type'],
                    price=price,
                    time_=update_date
                )
                info_log.info(f'POST:/imports Новый обьект id={item["id"]}, 200')
                if parent_id is not None:
                    go_up(parent_id, delta=price, time_update=update_date, flag_=item['type'] == 'OFFER')

        else:
            info_log.warning('POST:/imports Проблемы с отдельной структурой item')
            warning_log.warning(
                f'POST:/imports Проблемы с отдельной структурой item:\nitem={item}\n, 404')
            return json_error_import, 400
    return '', 200
