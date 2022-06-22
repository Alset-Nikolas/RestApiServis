import datetime
from base_functions import *
from app import app, db, ShopUnit


def test_no_valid_date(logger):
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


def test_no_valid_type(logger):
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


def test_no_valid_price(logger):
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


def test_no_valid_name(logger):
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


def test_no_valid_name_int(logger):
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


def test_no_valid_child(logger):
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


def test_valid_child(logger):
    '''Родителем OFFER - только CATEGORY'''
    update_node = {
        "items": [
            {
                "type": 'CATEGORY',
                "name": '3',
                "id": 'MY_ID',
                "parentId": None,
                "price": None
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
    assert status == 200, f"Expected HTTP status code 200, got {status}"
    logger.info(f'test_no_valid_name: passed')


def test_valid_name_str(logger):
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


def test_no_valid_id(logger):
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
        node = ShopUnit.query.filter_by(id=id_node).first()
        new_data = node.date + datetime.timedelta(days=add_days)
        update_node = {
            "items": [
                {
                    "type": node.type.type,
                    "name": node.name,
                    "id": node.id,
                    "parentId": node.parentId,
                    "price": node.price
                },
            ],
            "updateDate": new_data.strftime("%Y-%m-%dT%H:%M:%S.%f%z")[:-3] + 'Z'
        }
        status, x = request("/imports", method="POST", data=update_node)
        assert status == 200, f"Expected HTTP status code 200, got {status}"
        return new_data

    new_time = update_date()
    node = ShopUnit.query.filter_by(id=id_node).first()
    assert node.date == new_time, f"Expected datetime {new_time}, got {node.date}, id={id_node}"
    parent_id = node.parentId
    while parent_id is not None:
        parent = ShopUnit.query.filter_by(id=parent_id).first()
        assert parent.date == new_time, f"Expected datetime {new_time}, got {parent.date}, id={parent_id}"
        parent_id = parent.parentId


def test_price(id_node, add_price):
    def remember_old_price():
        return {x.id: x.price for x in ShopUnit.query.all()}

    def update_price():
        node = ShopUnit.query.filter_by(id=id_node).first()
        if node.price is None:
            new_price = 1000
        else:
            new_price = node.price + add_price
        update_node = {
            "items": [
                {
                    "type": node.type.type,
                    "name": node.name,
                    "id": id_node,
                    "parentId": node.parentId,
                    "price": new_price
                },
            ],
            "updateDate": str(node.date.strftime('%Y-%m-%dT%H:%M:%S.%f%Z')[:-3] + 'Z')
        }
        status, x = request("/imports", method="POST", data=update_node)
        if node.type.type == 'OFFER':
            assert status == 200, f"Expected HTTP status code 200, got {status}"
        else:
            assert status == 400, f"Expected HTTP status code 400, got {status}"

    def check_child(node_id, old_price):
        childs = ShopUnit.query.filter_by(parentId=node_id).all()
        if childs == []:
            return
        for child in childs:
            id_child = child.node_id
            assert child.price == old_price[
                id_child], f"Expected price {old_price[id_child].price}, got {child.price}, id={id_child}"
            check_child(id_child, old_price)

    old_price = remember_old_price()
    update_price()
    node = ShopUnit.query.filter_by(id=id_node).first()
    if node.type.type == 'OFFER':
        assert node.price == old_price[
            id_node] + add_price, f"Expected price {node.price}, got {old_price[id_node] + add_price}, id={id_node}"




def update_parent(node_id, new_parent_id):

    node = ShopUnit.query.filter_by(id=node_id).first()
    assert node is not None, f'нет такого id={node_id}'
    old_parent_id = node.parentId
    update_node = {
        "items": [
            {
                "type": node.type.type,
                "name": node.name,
                "id": node_id,
                "parentId": new_parent_id,
                "price": node.price
            }
        ],
        "updateDate": str(node.date.strftime('%Y-%m-%dT%H:%M:%S.%f%Z')[:-3] + 'Z')
    }
    status, x = request("/imports", method="POST", data=update_node)
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    status, response = request(f"/nodes/{node_id}", json_response=True)
    assert status == 200, f"Expected HTTP status code 200, got {status}"
    assert response['parentId'] == new_parent_id
    new_parent = ShopUnit.query.filter_by(id=new_parent_id).first()
    old_parent = ShopUnit.query.filter_by(id=old_parent_id).first()
    if new_parent is not None:
        assert node_id in new_parent.children, f"У нового родителя нет такого ребенка id_child={node_id}, if_parent={new_parent_id}"
    if old_parent is not None:
        if old_parent != new_parent:
            assert node_id not in old_parent.children, f"У старого родителя остался ребенок id_child={node_id}, if_parent={old_parent}"
        else:
            assert node_id  in old_parent.children, f"Родитель не менялся id_child={node_id}, if_parent={old_parent}"






def test_valid_update_parent(logger):
    '''Если у категории или товара обновить родителя на'''
    clear_bd(logger)
    test_import(logger)
    update_parent(node_id='98883e8f-0507-482f-bce2-2fb306cf6483', new_parent_id=None)
    update_parent(node_id='98883e8f-0507-482f-bce2-2fb306cf6483', new_parent_id='069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')
    update_parent(node_id='98883e8f-0507-482f-bce2-2fb306cf6483', new_parent_id='d515e43f-f3f6-4471-bb77-6b455017a2d2')
    update_parent(node_id='73bc3b36-02d1-4245-ab35-3106c9ee1c65', new_parent_id='1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2')
    update_parent(node_id='73bc3b36-02d1-4245-ab35-3106c9ee1c65', new_parent_id='069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')
    update_parent(node_id='74b81fda-9cdc-4b63-8927-c978afed5cf4', new_parent_id='069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')



def test_all(logger):
    clear_bd(logger)
    test_import(logger)
    all_node_ids = [x.id for x in ShopUnit.query.all()]
    for i, node in enumerate(all_node_ids):
        test_valid_date(node, add_days=i + 1)
    logger.info(f'test_date: passed')
    for i, node in enumerate(all_node_ids):
        test_price(node, add_price=i + 1)
    logger.info(f'test_price: passed')
    test_no_valid_date(logger)
    test_no_valid_type(logger)
    test_no_valid_price(logger)
    test_no_valid_name(logger)
    test_no_valid_id(logger)
    test_no_valid_name_int(logger)
    test_valid_name_str(logger)
    test_no_valid_child(logger)
    test_valid_child(logger)

    test_valid_update_parent(logger)

if __name__ == "__main__":
    logger = create_logging()
    # test_all(logger)
    test_import(logger)
