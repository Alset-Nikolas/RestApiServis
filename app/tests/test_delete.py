from base_functions import *
from app import app, db, ShopUnit
START_TREE = {
  "children": [
    {
      "children": [
        {
          "children": None,
          "date": "2022-02-05T12:00:00.000Z",
          "id": "863e1a7a-1304-42ae-943b-179184c077e3",
          "name": "jPhone 13",
          "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
          "price": 79999,
          "type": "OFFER"
        },
        {
          "children": None,
          "date": "2022-02-06T12:00:00.000Z",
          "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
          "name": "Xomi\u0430 Readme 10",
          "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
          "price": 59999,
          "type": "OFFER"
        }
      ],
      "date": "2022-02-06T12:00:00.000Z",
      "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
      "name": "\u0421\u043c\u0430\u0440\u0442\u0444\u043e\u043d\u044b",
      "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
      "price": 139999,
      "type": "CATEGORY"
    },
    {
      "children": [
        {
          "children": None,
          "date": "2022-02-09T12:00:00.000Z",
          "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
          "name": "Samson 70\" LED UHD Smart",
          "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
          "price": 32999,
          "type": "OFFER"
        },
        {
          "children": None,
          "date": "2022-02-10T12:00:00.000Z",
          "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
          "name": "Phyllis 50\" LED UHD Smarter",
          "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
          "price": 49999,
          "type": "OFFER"
        },
        {
          "children": None,
          "date": "2022-02-11T15:00:00.000Z",
          "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
          "name": "Goldstar 65\" LED UHD LOL Very Smart",
          "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
          "price": 69999,
          "type": "OFFER"
        }
      ],
      "date": "2022-02-11T15:00:00.000Z",
      "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
      "name": "\u0422\u0435\u043b\u0435\u0432\u0438\u0437\u043e\u0440\u044b",
      "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
      "price": 101998,
      "type": "CATEGORY"
    }
  ],
  "date": "2022-02-06T12:00:00.000Z",
  "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
  "name": "\u0422\u043e\u0432\u0430\u0440\u044b",
  "parentId": None,
  "price": 231796,
  "type": "CATEGORY"
}


def check_children(delete_id):
    children_del_node = ShopUnit.query.filter_by(parentId=delete_id).all()
    for child in children_del_node:
        id_child = child.node_id
        status, _ = request(f"/nodes/{id_child}", json_response=True)
        assert status == 404, f"Expected HTTP status code 404, got {status}"

def check_parent(id_node, parent_info_before_del, del_node_before_del):
    parent = ShopUnit.query.filter_by(id=parent_info_before_del['id']).first()
    if del_node_before_del['type'] == 'OFFER':
        cop = parent_info_before_del['children'].copy()
        cop.pop(cop.index(id_node))
        assert sorted(parent.children) == sorted(cop), f'После удаления OFFER ожидалось {sorted(cop)}, получили {sorted(parent.children)} ,Параметры родителя: name={parent.name}, id={parent.id}'
    else:
        cop =  sorted(list(set(parent_info_before_del['children']) - set(del_node_before_del['children'])))
        assert parent.children == cop, f'у предка {parent.name}  дети={parent.children}, а должно быть {cop},Параметры родителя: name={parent.name}, id={parent.id}'

def check_parents(id_node, ancestors_info_before_del, del_node_before_del):
    for parent_info_before_del in ancestors_info_before_del:
        check_parent(id_node, parent_info_before_del, del_node_before_del)
    return


def delete_node(delete_id):
    del_node = ShopUnit.query.filter_by(id=delete_id).first()
    parent_id = del_node.parentId

    del_node_before_del = {
        'type': del_node.type.type,
        'children': [] if del_node.children is None else list(del_node.children ),
        'price': del_node.price,
    }
    ancestors_info_before_del = []
    while parent_id is not None:
        parent = ShopUnit.query.filter_by(id=parent_id).first()
        parent_info_before_del = {
            'id': parent_id,
            'price': parent.price,
            'children': list(parent.children),
        }
        ancestors_info_before_del.append(parent_info_before_del)
        parent_id = parent.parentId

    status, _ = request(f"/delete/{delete_id}", method="DELETE")
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    status, _ = request(f"/nodes/{delete_id}", json_response=True)
    assert status == 404, f"Expected HTTP status code 404, got {status}"

    return ancestors_info_before_del, del_node_before_del


def test_valid_delete(id_node):
    parent_info_before_del, del_node_before_del = delete_node(id_node)
    check_parents(id_node, parent_info_before_del, del_node_before_del)
    check_children(id_node)


def test_no_valid_delete():
    ids = ["null"]
    for delete_id in ids:
        status, _ = request(f"/delete/{delete_id}", method="DELETE")
        assert status == 400, f"Expected HTTP status code 400, got {status}"

    id_ = ['zzzzzzzzzzzzzzzzzzzzzzz']
    status, _ = request(f"/delete/{id_}", method="DELETE")
    assert status == 404, f"Expected HTTP status code 404, got {status}"

    clear_bd(logger)
    test_import(logger)
    test_valid_delete(ROOT_ID)

    status, _ = request(f"/delete/{ROOT_ID}", method="DELETE")
    assert status == 404, f"Expected HTTP status code 404, got {status}"




if __name__ == "__main__":
    logger = create_logging()
    clear_bd(logger)
    test_import(logger)
    add_new_category(logger)
    for node_id in [x.id for x in ShopUnit.query.all()]:
        test_valid_delete(node_id)
        clear_bd(logger)
        test_import(logger)
        add_new_category(logger)
    logger.info('check_delete: passed')
    test_no_valid_delete()


