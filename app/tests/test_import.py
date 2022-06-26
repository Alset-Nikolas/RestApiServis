import datetime
from base_functions import *
from components.schemas.ShopUnit import ShopUnit
from my_logs.logg import info_log


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


def test_no_valid_child_1(logger):
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
                "type": 'CATEGORY',
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
    logger.info(f'test_no_valid_child_1: passed')


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


def test_valid_child_1(logger):
    '''Родителем OFFER - только CATEGORY'''
    update_node = {
        "items": [
            {
                "type": 'OFFER',
                "name": '2',
                "id": '12*10' * 3,
                "parentId": None,
                "price": 1
            },

        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    }
    status, x = request("/imports", method="POST", data=update_node)
    assert status == 200, f"Expected HTTP status code 200, got {status}"
    logger.info(f'test_valid_child_1: passed')


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


def get_date(id):
    status, response = request(f"/nodes/{id}", json_response=True)
    assert status == 200
    if response['children']:
        children = [x['id'] for x in response['children']]
    else:
        children = None
    return response['date'], response['parentId'], children


def check_date(id_check, time_update):
    date, parent_id, children = get_date(id_check)
    assert date == time_update[
                   :-6] + '000Z', f"Expected datetime time_update={time_update[:-6] + '000Z'}, got node.date={date}, id={id_check}"

    while parent_id is not None:
        status, response = request(f"/nodes/{parent_id}", json_response=True)
        assert status == 200
        if status != 200:
            break
        date = response['date']
        assert date == time_update[
                       :-6] + '000Z', f"Expected datetime time_update={time_update[:-6] + '000Z'}, got parent.date={date}, id={parent_id}"
        parent_id = response['parentId']


def test_valid_date(id_node, add_days):
    def update_date():
        node = ShopUnit.query.filter_by(id=id_node).first()
        new_data = node.date + datetime.timedelta(days=add_days)
        update_node = {
            "items": [
                {
                    "type": node.type,
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
        return new_data.strftime("%Y-%m-%dT%H:%M:%S.%f%z")[:-1]

    new_time = update_date()
    check_date(id_node, new_time)


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
                    "type": node.type,
                    "name": node.name,
                    "id": id_node,
                    "parentId": node.parentId,
                    "price": new_price
                },
            ],
            "updateDate": str(node.date.strftime('%Y-%m-%dT%H:%M:%S.%f%Z')[:-3] + 'Z')
        }
        status, x = request("/imports", method="POST", data=update_node)
        if node.type == 'OFFER':
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
    if node.type == 'OFFER':
        assert node.price == old_price[
            id_node] + add_price, f"Expected price {node.price}, got {old_price[id_node] + add_price}, id={id_node}"


def update_parent(node_id, new_parent_id):
    node = ShopUnit.query.filter_by(id=node_id).first()
    assert node is not None, f'нет такого id={node_id}'
    old_parent_id = node.parentId
    update_node = {
        "items": [
            {
                "type": node.type,
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
            assert node_id in old_parent.children, f"Родитель не менялся id_child={node_id}, if_parent={old_parent}"


def test_valid_update_parent(logger):
    '''Если у категории или товара обновить родителя на другого родителя '''
    clear_bd(logger)
    test_import(logger)
    update_parent(node_id='98883e8f-0507-482f-bce2-2fb306cf6483', new_parent_id=None)
    update_parent(node_id='98883e8f-0507-482f-bce2-2fb306cf6483', new_parent_id='069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')
    update_parent(node_id='98883e8f-0507-482f-bce2-2fb306cf6483', new_parent_id='d515e43f-f3f6-4471-bb77-6b455017a2d2')
    update_parent(node_id='73bc3b36-02d1-4245-ab35-3106c9ee1c65', new_parent_id='1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2')
    update_parent(node_id='73bc3b36-02d1-4245-ab35-3106c9ee1c65', new_parent_id='069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')
    update_parent(node_id='74b81fda-9cdc-4b63-8927-c978afed5cf4', new_parent_id='069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')


def id_conversation(id):
    return f"{str(id)}-10000"


def get_all_descendants(node_id):
    # {x.id: x.price for x in ShopUnit.query.all()}
    node = ShopUnit.query.filter_by(id=node_id).first()
    parents = [node_id]
    ans = []
    box = []
    while len(parents) > 0:
        for parent_id in parents:
            parent = ShopUnit.query.filter_by(id=parent_id).first()
            if parent.children:
                ans += parent.children
                box += parent.children
        parents = box
        box = []

    return ans


def test_check_swap_parents(children_id, parents_id):
    '''
        Функция проверки замены родителя.
    '''
    parent_id_after_filter = parents_id
    for node_id in children_id:  # для каждого узла
        node = ShopUnit.query.filter_by(id=node_id).first()
        old_parent_id = node.parentId  # запоминаем его родителя
        old_parent = ShopUnit.query.filter_by(id=old_parent_id).first()
        if node.type == 'CATEGORY':
            parent_id_after_filter = list(set(parents_id) - set(get_all_descendants(
                node_id)))  # Если мы смещаем категорию, то его детей нельзя рассматривать как нового родителя
        for new_parent_id in parent_id_after_filter:  # из каждой категории
            if new_parent_id == node_id:
                continue
            print(node_id, old_parent_id, new_parent_id, parent_id_after_filter)
            new_parent = ShopUnit.query.filter_by(id=new_parent_id).first()  # формируем нового родителя

            if old_parent and new_parent:  # назначаем новое время для проверки
                new_date = max(old_parent.date, new_parent.date) + datetime.timedelta(days=1)
            elif old_parent:
                new_date = old_parent.date + datetime.timedelta(days=1)
            elif new_parent:
                new_date = new_parent.date + datetime.timedelta(days=1)
            else:
                new_date = node.date + datetime.timedelta(days=1)
            update_node = {
                "items": [
                    {
                        "type": node.type,
                        "name": node.name,
                        "id": node_id,
                        "parentId": new_parent_id,
                        "price": node.price
                    }
                ],
                "updateDate": new_date.strftime(TIME_FORMAT)[:-3] + 'Z'
            }
            status, x = request("/imports", method="POST", data=update_node)  # меняем родителя
            assert status == 200, f"Expected HTTP status code 200, got {status}"
            old_parent_children = []
            new_parent_children = []
            if old_parent:
                check_date(old_parent_id, new_date.strftime(TIME_FORMAT))  # проверяем время
                _, _, old_parent_children = get_date(old_parent_id)

            if new_parent:
                check_date(new_parent_id, new_date.strftime(TIME_FORMAT))  # проверяем время
                _, _, new_parent_children = get_date(new_parent_id)

            if old_parent_id == new_parent_id:  # если родитель не менялся
                if new_parent_children:
                    assert node_id in new_parent_children  # у старого родителя должен остаться этот ребенок
            else:
                if old_parent_children:
                    assert node_id not in old_parent_children  # у старого родителя не должен остаться этот ребенок
                if new_parent_children:
                    assert node_id in new_parent_children  # у нового должен

            if old_parent:
                update_node = {
                    "items": [
                        {
                            "type": node.type,
                            "name": node.name,
                            "id": node_id,
                            "parentId": old_parent_id,
                            "price": node.price
                        }
                    ],
                    "updateDate": new_date.strftime(TIME_FORMAT)[:-3] + 'Z'
                }
                status, x = request("/imports", method="POST", data=update_node)
                assert status == 200, f"Expected HTTP status code 200, got {status}"  # возвращаем все как было (старому родителю)


def test_import_random_tree(logger):
    '''
        Проверка случайного дерева
    Идея: Проверить изменение родителей - для кажого узла OFFER перебрать все комбинации смены родителя '''
    tree, last_id_category, last_id_offer, date_first, date_end = create_random_tree()
    clear_bd(logger)
    import_tree(logger, tree)
    all_category_id = [id_conversation(id_category) for id_category in range(1, last_id_category)]  # id всех категорий
    all_offer_id = [id_conversation(id_offer) for id_offer in range(-1, last_id_offer, -1)]  # id всех offers
    test_check_swap_parents(all_offer_id + all_category_id,
                            all_category_id)  # дочерним узлом мб любой, а родителем только категория

    for category_id in all_category_id + all_offer_id:
        node = ShopUnit.query.filter_by(id=category_id).first()
        for offer_id in all_offer_id:
            update_node = {
                "items": [
                    {
                        "type": node.type,
                        "name": node.name,
                        "id": category_id,
                        "parentId": offer_id,
                        "price": node.price
                    }
                ],
                "updateDate": node.date.strftime(TIME_FORMAT)[:-3] + 'Z'
            }
            status, x = request("/imports", method="POST", data=update_node)
            assert status == 400, f"Expected HTTP status code 200, got {status}"


def test_all(logger):
    # clear_bd(logger)
    # test_import(logger)
    # all_node_ids = [x.id for x in ShopUnit.query.all()]
    # for i, node in enumerate(all_node_ids):
    #     test_valid_date(node, add_days=i + 1)
    # logger.info(f'test_date: passed')
    # for i, node in enumerate(all_node_ids):
    #     test_price(node, add_price=i + 1)
    # logger.info(f'test_price: passed')
    # test_valid_child_1(logger)
    # test_no_valid_date(logger)
    # test_no_valid_type(logger)
    # test_no_valid_child_1(logger)
    # test_no_valid_price(logger)
    # test_no_valid_name(logger)
    # test_no_valid_id(logger)
    # test_no_valid_name_int(logger)
    # test_valid_name_str(logger)
    # test_no_valid_child(logger)
    # test_valid_child(logger)
    # test_valid_update_parent(logger)

    n = 1
    logger.info(f'test random_tree n={n}')
    for i in range(n):
        logger.info(f'test random_tree {i}/{n}')
        test_import_random_tree(logger)
    logger.info(f'test random_tree passed')


if __name__ == "__main__":
    logger = info_log
    test_all(logger)
