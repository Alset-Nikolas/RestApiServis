from enrollment.tests.base_functions import *

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
        children = NodeTree.query.filter_by(parentId=id_leaf).all()
        node = NodeTree.query.filter_by(node_id=id_leaf).first()
        q_children = len(children)
        if q_children == 0:
            assert response['children'] is None
            assert response['price'] == 0
        else:
            assert q_children == len(response['children'])

            assert response['price'] == sum([x.price for x in children])//node.childs
    id_parent = response['parentId']
    check_response_node(id_parent)


if __name__ == "__main__":
    logger = create_logging()
    clear_bd(logger)
    test_import(logger)
    add_new_category(logger)
    for id_ in [x.node_id for x in NodeTree.query.filter_by(childs=0).all()]:
        check_response_node(id_)
    logger.info('check_response_node: passed')
