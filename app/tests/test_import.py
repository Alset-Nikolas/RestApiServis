import datetime
from base_functions import *


def test_no_valid_date():
    '''Проверка на валидность updateDate. Ожидаем только iso формат'''
    update_node = {
        "items": [
            {
                "type": 'OFFER',
                "name": 'probe1',
                "id": '12*10' * 3,
                "parentId": None,
                "price": 10
            },
        ],
        "updateDate": '2022.11.20'
    }
    status, x = request("/imports", method="POST", data=update_node)
    assert status == 400, f"Expected HTTP status code 400, got {status}"
    logger.info(f'test_no_valid_date: passed')


def test_no_valid_type():
    '''Типы у обьектов могут быть только OFFER или CATEGORY'''
    update_node = {
        "items": [
            {
                "type": 'type',
                "name": 'probe1',
                "id": '12*10' * 3,
                "parentId": None,
                "price": 10
            },
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    }
    status, x = request("/imports", method="POST", data=update_node)
    assert status == 400, f"Expected HTTP status code 400, got {status}"
    logger.info(f'test_no_valid_type: passed')


def test_no_valid_price():
    '''price >=0 '''
    update_node = {
        "items": [
            {
                "type": 'type',
                "name": 'probe1',
                "id": '12*10' * 3,
                "parentId": None,
                "price": -10
            },
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    }
    status, x = request("/imports", method="POST", data=update_node)
    assert status == 400, f"Expected HTTP status code 400, got {status}"
    logger.info(f'test_no_valid_price: passed')


def test_no_valid_name():
    '''name != None'''
    update_node = {
        "items": [
            {
                "type": 'type',
                "name": None,
                "id": '12*10' * 3,
                "parentId": None,
                "price": 1
            },
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    }
    status, x = request("/imports", method="POST", data=update_node)
    assert status == 400, f"Expected HTTP status code 400, got {status}"
    logger.info(f'test_no_valid_name: passed')


def test_no_valid_name_int():
    update_node = {
        "items": [
            {
                "type": 'type',
                "name": 1,
                "id": '12*10' * 3,
                "parentId": None,
                "price": 1
            },
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    }
    status, x = request("/imports", method="POST", data=update_node)
    assert status == 400, f"Expected HTTP status code 400, got {status}"
    logger.info(f'test_no_valid_name: passed')


def test_no_valid_child():
    '''Родителем OFFER - только CATEGORY'''
    update_node = {
        "items": [
            {
                "type": 'OFFER',
                "name": '3',
                "id": 'MY_ID',
                "parentId": None,
                "price": 1
            },
            {
                "type": 'OFFER',
                "name": '2',
                "id": '12*10' * 3,
                "parentId": 'MY_ID',
                "price": 1
            },

        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    }
    status, x = request("/imports", method="POST", data=update_node)
    assert status == 400, f"Expected HTTP status code 400, got {status}"
    logger.info(f'test_no_valid_name: passed')


def test_valid_child():
    '''Родителем OFFER - только CATEGORY'''
    update_node = {
        "items": [
            {
                "type": 'CATEGORY',
                "name": '3',
                "id": 'MY_ID',
                "parentId": None,
                "price": 1
            },
            {
                "type": 'OFFER',
                "name": '2',
                "id": '12*10' * 3,
                "parentId": 'MY_ID',
                "price": 1
            },

        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    }
    status, x = request("/imports", method="POST", data=update_node)
    assert status == 200, f"Expected HTTP status code 400, got {status}"
    logger.info(f'test_no_valid_name: passed')


def test_valid_name_str():
    update_node = {
        "items": [
            {
                "type": 'OFFER',
                "name": '1',
                "id": '12*10' * 3,
                "parentId": None,
                "price": 1
            },
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    }
    status, x = request("/imports", method="POST", data=update_node)
    assert status == 200, f"Expected HTTP status code 400, got {status}"
    logger.info(f'test_valid_name_str: passed')


def test_no_valid_id():
    '''Дубликатов быть не может'''
    update_node = {
        "items": [
            {
                "type": 'type',
                "name": '1',
                "id": '12*10' * 3,
                "parentId": None,
                "price": 1
            },
            {
                "type": 'type1',
                "name": '2',
                "id": '12*10' * 3,
                "parentId": None,
                "price": 1
            },
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    }
    status, x = request("/imports", method="POST", data=update_node)
    assert status == 400, f"Expected HTTP status code 400, got {status}"
    logger.info(f'test_no_valid_id: passed')


def test_valid_date(id_node, add_days):
    def update_date():
        node = NodeTree.query.filter_by(node_id=id_node).first()
        new_time = node.time_ + datetime.timedelta(days=add_days)
        update_node = {
            "items": [
                {
                    "type": node.type_,
                    "name": node.name,
                    "id": id_node,
                    "parentId": node.parentId,
                    "price": node.price
                },
            ],
            "updateDate": new_time.strftime("%Y-%m-%dT%H:%M:%S.%f%z")[:-3] + 'Z'
        }
        status, x = request("/imports", method="POST", data=update_node)
        assert status == 200, f"Expected HTTP status code 200, got {status}"
        return new_time

    new_time = update_date()
    node = NodeTree.query.filter_by(node_id=id_node).first()
    assert node.time_ == new_time, f"Expected datetime {new_time}, got {node.time_}, id={id_node}"
    parent_id = node.parentId
    while parent_id is not None:
        parent = NodeTree.query.filter_by(node_id=parent_id).first()
        assert parent.time_ == new_time, f"Expected datetime {new_time}, got {parent.time_}, id={parent_id}"
        parent_id = parent.parentId


def test_price(id_node, add_price):
    def remember_old_price():
        return {x.node_id: x.price for x in NodeTree.query.all()}

    def update_price():
        node = NodeTree.query.filter_by(node_id=id_node).first()
        new_price = node.price + add_price
        update_node = {
            "items": [
                {
                    "type": node.type_,
                    "name": node.name,
                    "id": id_node,
                    "parentId": node.parentId,
                    "price": new_price
                },
            ],
            "updateDate": str(node.time_.strftime('%Y-%m-%dT%H:%M:%S.%f%Z')[:-3] + 'Z')
        }
        status, x = request("/imports", method="POST", data=update_node)
        assert status == 200, f"Expected HTTP status code 200, got {status}"

    def check_child(node_id, old_price):
        childs = NodeTree.query.filter_by(parentId=node_id).all()
        if childs == []:
            return
        for child in childs:
            id_child = child.node_id
            assert child.price == old_price[
                id_child], f"Expected price {old_price[id_child].price}, got {child.price}, id={id_child}"
            check_child(id_child, old_price)

    old_price = remember_old_price()
    update_price()

    node = NodeTree.query.filter_by(node_id=id_node).first()
    assert node.price == old_price[
        id_node] + add_price, f"Expected price {node.price}, got {old_price[id_node] + add_price}, id={id_node}"
    parent_id = node.parentId
    while parent_id is not None:
        parent = NodeTree.query.filter_by(node_id=parent_id).first()

        assert parent.price == old_price[
            parent_id] + add_price, f"Expected price {parent.price}, got {old_price[parent_id] + add_price}, id={parent_id}"
        parent_id = parent.parentId
    check_child(id_node, old_price)


def update_parent(node_id, new_parent_id):
    def remember_state():
        return {x.node_id: {'price': x.price, 'childs': x.childs} for x in NodeTree.query.all()}

    node = NodeTree.query.filter_by(node_id=node_id).first()
    assert node is not None, f'нет такого id={node_id}'
    old_parent_id = node.parentId
    update_node = {
        "items": [
            {
                "type": node.type_,
                "name": node.name,
                "id": node_id,
                "parentId": new_parent_id,
                "price": node.price
            }
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    }
    remember_table = remember_state()
    status, x = request("/imports", method="POST", data=update_node)
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    status, response = request(f"/nodes/{node_id}", json_response=True)
    assert status == 200, f"Expected HTTP status code 200, got {status}"
    assert response['parentId'] == new_parent_id

    if node.type_ == 'OFFER':
        diff_child = 1
    else:
        diff_child = node.childs

    while old_parent_id is not None:
        old_parent_node = NodeTree.query.filter_by(node_id=old_parent_id).first()
        remember_table[old_parent_id]['childs'] -= diff_child
        remember_table[old_parent_id]['price'] -= node.price
        old_parent_id = old_parent_node.parentId

    while new_parent_id is not None:
        new_parent_node = NodeTree.query.filter_by(node_id=new_parent_id).first()
        remember_table[new_parent_id]['childs'] += diff_child
        remember_table[new_parent_id]['price'] += node.price
        new_parent_id = new_parent_node.parentId

    assert remember_table == remember_state()


def test_valid_update_parent():
    '''Если у категории или товара обновить родителя на'''
    clear_bd(logger)
    test_import(logger)
    update_parent(node_id='98883e8f-0507-482f-bce2-2fb306cf6483', new_parent_id=None)
    update_parent(node_id='98883e8f-0507-482f-bce2-2fb306cf6483', new_parent_id='069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')
    update_parent(node_id='98883e8f-0507-482f-bce2-2fb306cf6483', new_parent_id='d515e43f-f3f6-4471-bb77-6b455017a2d2')
    update_parent(node_id='73bc3b36-02d1-4245-ab35-3106c9ee1c65', new_parent_id='1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2')
    update_parent(node_id='73bc3b36-02d1-4245-ab35-3106c9ee1c65', new_parent_id='069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')
    update_parent(node_id='74b81fda-9cdc-4b63-8927-c978afed5cf4', new_parent_id='069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')




if __name__ == "__main__":
    logger = create_logging()
    clear_bd(logger)
    test_import(logger)
    all_node_ids = [x.node_id for x in NodeTree.query.all()]
    for i, node in enumerate(all_node_ids):
        test_valid_date(node, add_days=i + 1)
    logger.info(f'test_date: passed')
    for i, node in enumerate(all_node_ids):
        test_price(node, add_price=i + 1)
    logger.info(f'test_price: passed')

    test_no_valid_date()
    test_no_valid_type()
    test_no_valid_price()
    test_no_valid_name()
    test_no_valid_id()
    test_no_valid_name_int()
    test_valid_name_str()
    test_no_valid_child()
    test_valid_child()

    test_valid_update_parent()

