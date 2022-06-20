import datetime
from enrollment.tests.base_functions import *


def test_no_valid_date():
    '''Проверка на валидность даты ->updateDate. Ожидаем только iso формат'''
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

    #TODO ЕСЛИ КАТЕГОРИЯ ПОЛЕ PRICE ПРОВЕРКА НАNone