'''
    Набор функций, которые применяются в рамках hanlers
'''
from app import NodeTree

def is_category(node) -> bool:
    '''Является тип узла - категория'''
    return node.type_ == 'CATEGORY'


def calc_price(price:int, childs:int)->int:
    '''Рассчкт средней стоимости'''
    if childs==0:
        return price
    return price//childs


def get_info(id_node:str) -> set:
    '''Вернуть ниформацию о узле и его детей'''
    node = NodeTree.query.filter_by(node_id=id_node).first()
    ans = dict()
    #todo
    ans["childs"] = node.childs
    ans["type"] = node.type_
    ans["name"] = node.name
    ans["id"] = id_node
    ans["parentId"] = node.parentId
    ans["date"] = str(node.time_.strftime('%Y-%m-%dT%H:%M:%S.%f%Z')[:-3]+'Z')
    ans['children'] = []
    childs = NodeTree.query.filter_by(parentId=node.node_id).all()
    if childs!= []:
        for child in childs:
            ans['children'].append(get_info(child.node_id))
    ans["price"] = calc_price(node.price, node.childs)
    if not is_category(node):
        ans['children'] = None
    return ans
