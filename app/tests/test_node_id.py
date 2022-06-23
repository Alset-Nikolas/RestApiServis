from base_functions import *
from components.schemas.ShopUnit import ShopUnit


def check_response_node(id_leaf):
    if id_leaf is None:
        return
    status, response = request(f"/nodes/{id_leaf}", json_response=True)
    assert status == 200, f"Expected HTTP status code 200, got {status}"
    assert response['type'] in ['OFFER', 'CATEGORY']
    if response['type'] == 'OFFER':
        assert response['price'] >= 0, f'price > 0 , price={response["price"]}'
        assert response['name'] is not None, f"name is None"
        assert response['children'] is None, f"children is not None"
    else:
        node = ShopUnit.query.filter_by(id=id_leaf).first()
        children = node.children

        q_offer = 0
        sum_ =0
        box = []
        while children != []:
            for child_id in children:
                child = ShopUnit.query.filter_by(id=child_id).first()
                if child.type.type=='OFFER':
                    q_offer+=1
                    sum_ += child.price
                else:
                    box += child.children
            children = box
            box = []

        assert response['price'] == sum_//q_offer,f'Ждали сумму={sum_//q_offer} Получили={response["price"]} id={id_leaf}'
    id_parent = response['parentId']
    check_response_node(id_parent)


def test_all(logger):
    clear_bd(logger)
    test_import(logger)
    add_new_category(logger)
    for id_ in [x.id for x in ShopUnit.query.filter_by(children=None).all()]:
        check_response_node(id_)
    logger.info('check_response_node: passed')


if __name__ == "__main__":
    logger = create_logging()
    test_all(logger)
