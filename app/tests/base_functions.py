import json
import urllib.error
import urllib.parse
import urllib.request
import logging
from app import  db
from app import app, db, ShopUnit, ShopUnitImport, ShopUnitImportRequest, Error, ShopUnit, ShopUnitType

API_BASEURL = "http://localhost:5000"
ROOT_ID = "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"

IMPORT_BATCHES = [
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Смартфоны",
                "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "jPhone 13",
                "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 79999
            },
            {
                "type": "OFFER",
                "name": "Xomiа Readme 10",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 59999
            }
        ],
        "updateDate": "2022-02-02T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Телевизоры",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "Samson 70\" LED UHD Smart",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 32999
            },
            {
                "type": "OFFER",
                "name": "Phyllis 50\" LED UHD Smarter",
                "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 49999
            }
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "Goldstar 65\" LED UHD LOL Very Smart",
                "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 69999
            }
        ],
        "updateDate": "2022-02-03T15:00:00.000Z"
    }
]





def request(path, method="GET", data=None, json_response=False):
    try:
        params = {
            "url": f"{API_BASEURL}{path}",
            "method": method,
            "headers": {},
        }

        if data:
            params["data"] = json.dumps(
                data, ensure_ascii=False).encode("utf-8")
            params["headers"]["Content-Length"] = len(params["data"])
            params["headers"]["Content-Type"] = "application/json"

        req = urllib.request.Request(**params)

        with urllib.request.urlopen(req) as res:
            res_data = res.read().decode("utf-8")
            if json_response:
                res_data = json.loads(res_data)
            return (res.getcode(), res_data)
    except urllib.error.HTTPError as e:
        return (e.getcode(), None)


def create_logging():
    '''Создание логирования для теста'''
    logger = logging.getLogger('test_log')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
#
# def check_bd(logger):
#     '''Проверка значений в таблице NodeTree'''
#     q_items = 0
#     for data in IMPORT_BATCHES:
#         time = data['updateDate']
#         items = data['items']
#         for item in items:
#             node_id = item['id']
#             q_items += 1
#             ans_base = NodeTree.query.filter_by(node_id=node_id).all()
#             assert len(ans_base) == 1
#             ans_base = ans_base[0]
#             assert item['type'] == ans_base.type_
#             assert item['name'] == ans_base.name
#             assert item['parentId'] == ans_base.parentId
#     assert len(NodeTree.query.all()) == q_items, f'В таблице записей {len(NodeTree.query.all())}, '
#     logger.info(f'check_bd: passed')
#
def clear_bd(logger):
    '''Очистка таблицы NodeTree'''
    for node in ShopUnit.query.all():
        db.session.delete(node)
    db.session.commit()
    assert len(ShopUnit.query.all()) == 0
    logger.info(f'clear_bd: passed')

def test_import(logger):
    '''Заполнение таблицы значениями для теста'''
    for index, batch in enumerate(IMPORT_BATCHES):
        status, x = request("/imports", method="POST", data=batch)
        assert status == 200, f"Expected HTTP status code 200, got {status}"
    logger.info(f'test import passed.')
    # check_bd(logger)

def add_new_category(logger):
    id_tv_category = '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2'
    id_leaf = '21312312314123123123ZZZZZ'
    new_category = {
        "items": [
            {
                "type": 'CATEGORY',
                "name": 'Plasma tv',
                "id": f'21312312314123123123',
                "parentId": id_tv_category,
            },
            {
                "type": 'OFFER',
                "name": 'Телевизор Haier 43 Smart TV MX',
                "id": id_leaf,
                "parentId": '21312312314123123123',
                "price": 29999
            },
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    }
    status, x = request("/imports", method="POST", data=new_category)
    assert status == 200, f"Expected HTTP status code 200, got {status}"
    logger.info('Добавали новую категорию Plasma tv')
    return id_leaf