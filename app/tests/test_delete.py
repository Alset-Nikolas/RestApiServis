from base_functions import *
from components import ShopUnitStatistic
from components.schemas.ShopUnit import ShopUnit
from sqlalchemy import func

def check_children(delete_id, date):
    children_del_node = ShopUnit.query.filter_by(parentId=delete_id).all()
    for id_child in [x.id for x in children_del_node]:
        status, _ = request(f"/nodes/{id_child}", json_response=True)
        assert status == 404, f"Expected HTTP status code 404, got {status}"
    if delete_id is not None:
        nodes_stat = ShopUnit.query.filter_by(parentId=delete_id).all()
        assert nodes_stat == [], f'Записи в таблице ShopUnit еще есть: (x_id, pa_parent_id)={[(x.id, x.parentId) for x in nodes_stat]}'
    if delete_id is not None:
        nodes_stat = ShopUnitStatistic.query.filter_by(parentId=delete_id).filter(func.DATE(ShopUnitStatistic.date) < date).all()
        assert nodes_stat == [], f'Записи в таблице ShopUnitStatistic еще есть: (x_id, pa_parent_id)={[(x.id, x.parentId) for x in nodes_stat]}'


def check_parent(id_node, parent_info_before_del):
    if parent_info_before_del is None:
        return
    parent = ShopUnit.query.filter_by(id=parent_info_before_del['id']).first()
    cop = parent_info_before_del['children'].copy()
    cop.pop(cop.index(id_node))
    assert sorted(parent.children) == sorted(
        cop), f'После удаления OFFER ожидалось {sorted(cop)}, получили {sorted(parent.children)} ,Параметры родителя: name={parent.name}, id={parent.id}'

def remove_ids_children(children_ids, ids):
    if ids is None:
        return
    box = []
    while len(children_ids) != 0:
        for ch_id in children_ids:
            ids.remove(int(ch_id[:-6]))
            ch = ShopUnit.query.filter_by(id=ch_id).first()
            if ch.children:
                box += ch.children
        children_ids = box
        box = []

def delete_node(delete_id, ids):
    del_node = ShopUnit.query.filter_by(id=delete_id).first()
    remove_ids_children(del_node.children, ids)
    date = del_node.date
    parent_id = del_node.parentId

    parent = ShopUnit.query.filter_by(id=parent_id).first()
    parent_info_before_del = None
    if parent is not None:
        parent_info_before_del = {
            'id': parent.id,
            'price': parent.price,
            'children': list(parent.children),
            'date':parent.date
        }

    status, _ = request(f"/delete/{delete_id}", method="DELETE")
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    status, _ = request(f"/nodes/{delete_id}", json_response=True)
    assert status == 404, f"Expected HTTP status code 404, got {status}"

    nodes_stat = ShopUnitStatistic.query.filter_by(id=delete_id).all()
    assert nodes_stat == [], f'Записи в таблице ShopUnitStatistic еще есть: {nodes_stat}'

    return parent_info_before_del, date


def test_valid_delete(id_node, ids=None):
    parent_info_before_del, date = delete_node(id_node, ids)
    check_parent(id_node, parent_info_before_del)
    check_children(id_node, date)


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


def test_delete_random_tree(logger):
    logger.info('test_delete_random_tree run')
    tree, last_id_category, last_id_offer, date_first, date_end = create_random_tree()
    import_tree(logger, tree)
    ids = set(range(last_id_offer+1, last_id_category, 1))
    ids.remove(0)
    while len(ids) != 0:
        param = ids.pop()
        node_id = f"{param}-10000"
        test_valid_delete(node_id, ids)
    logger.info('test_delete_random_tree passed')


if __name__ == "__main__":
    logger = create_logging()
    test_all(logger)
    # test_delete_random_tree(logger)