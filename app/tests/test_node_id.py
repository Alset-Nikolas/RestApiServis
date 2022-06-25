from base_functions import *
from components.schemas.ShopUnit import ShopUnit



def check_response_node(id_leaf):
    if id_leaf is None:
        return
    status, response = request(f"/nodes/{id_leaf}", json_response=True)
    assert status == 200, f"Expected HTTP status code 200, got {status}"
    assert response['type'] in ['OFFER', 'CATEGORY']
    assert check_time(response['date']), f'{response["date"]}'
    if response['type'] == 'OFFER':
        assert response['price'] >= 0, f'price > 0 , price={response["price"]}'
        assert response['name'] is not None, f"name is None"
        assert response['children'] is None, f"children is not None"
    else:
        node = ShopUnit.query.filter_by(id=id_leaf).first()
        children = node.children

        q_offer = 0
        sum_ = 0
        box = []
        while children != []:
            for child_id in children:
                child = ShopUnit.query.filter_by(id=child_id).first()
                if child.type == 'OFFER':
                    q_offer += 1
                    sum_ += child.price
                else:
                    box += child.children
            children = box
            box = []
        if q_offer == 0:
            if response['type'] == 'CATEGORY':
                assert response['price'] is None, f'id_problem={node.id} price={response["price"]}'
                assert len(response['children']) == len(node.children), f'Не совпадает кол-во детей должно={len(node.children)}, сечас={len(response["children"])} '
            else:
                assert response['children'] is None, f'id_problem={node.id} children={response["children"]}'
                assert response['price'] == node.price, f'id_problem={node.id} price={response["price"]}'
        else:
            assert response[
                       'price'] == sum_ // q_offer, f'Ждали сумму={sum_ // q_offer} Получили={response["price"]} id={id_leaf}'
    id_parent = response['parentId']
    check_response_node(id_parent)


def test_all(logger):
    clear_bd(logger)
    test_import(logger)
    add_new_category(logger)
    for id_ in [x.id for x in ShopUnit.query.filter_by(children=None).all()]:
        check_response_node(id_)
    logger.info('check_response_node: passed')


def test_node_id_random_tree(logger):
    logger.info('test_node_id_random_tree run')
    # tree, last_id_category, last_id_offer, date_first, date_end = create_random_tree()
    # import_tree(logger, tree)
    # + [x.id for x in ShopUnit.query.filter_by(
    #             children=[]).all()]
    for id_ in [x.id for x in ShopUnit.query.filter_by(type='OFFER').all()]:
        check_response_node(id_)
    logger.info('test_node_id_random_tree passed')


if __name__ == "__main__":
    logger = create_logging()
    # test_all(logger)
    test_node_id_random_tree(logger)
