from base_functions import *
from components import ShopUnitStatistic
from components.schemas.ShopUnit import ShopUnit


def check_children(delete_id):
    children_del_node = ShopUnit.query.filter_by(parentId=delete_id).all()
    for child in children_del_node:
        id_child = child.node_id
        status, _ = request(f"/nodes/{id_child}", json_response=True)
        assert status == 404, f"Expected HTTP status code 404, got {status}"

    nodes_stat = ShopUnitStatistic.query.filter_by(parentId=delete_id).all()
    assert nodes_stat == [], f'Записи в таблице ShopUnitStatistic еще есть: {nodes_stat}'


def check_parent(id_node, parent_info_before_del):
    if parent_info_before_del is None:
        return
    parent = ShopUnit.query.filter_by(id=parent_info_before_del['id']).first()
    cop = parent_info_before_del['children'].copy()
    cop.pop(cop.index(id_node))
    assert sorted(parent.children) == sorted(
        cop), f'После удаления OFFER ожидалось {sorted(cop)}, получили {sorted(parent.children)} ,Параметры родителя: name={parent.name}, id={parent.id}'



def delete_node(delete_id):
    del_node = ShopUnit.query.filter_by(id=delete_id).first()
    parent_id = del_node.parentId

    parent = ShopUnit.query.filter_by(id=parent_id).first()
    parent_info_before_del = None
    if parent is not None:
        parent_info_before_del = {
            'id': parent.id,
            'price': parent.price,
            'children': list(parent.children),
        }

    status, _ = request(f"/delete/{delete_id}", method="DELETE")
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    status, _ = request(f"/nodes/{delete_id}", json_response=True)
    assert status == 404, f"Expected HTTP status code 404, got {status}"

    nodes_stat = ShopUnitStatistic.query.filter_by(id=delete_id).all()
    assert nodes_stat == [], f'Записи в таблице ShopUnitStatistic еще есть: {nodes_stat}'


    return parent_info_before_del


def test_valid_delete(id_node):
    parent_info_before_del = delete_node(id_node)
    check_parent(id_node, parent_info_before_del)
    check_children(id_node)


def test_no_valid_delete(logger):
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


def test_all(logger):
    clear_bd(logger)
    test_import(logger)
    add_new_category(logger)
    for node_id in [x.id for x in ShopUnit.query.all()]:
        test_valid_delete(node_id)
        clear_bd(logger)
        test_import(logger)
        add_new_category(logger)
    logger.info('check_delete: passed')
    test_no_valid_delete(logger)
    logger.info('check_delete: test_no_valid_delete')


if __name__ == "__main__":
    logger = create_logging()
    test_all(logger)
