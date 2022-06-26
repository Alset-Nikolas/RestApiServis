import datetime
from db import db
from components.schemas.ShopUnitImport import ShopUnitImport
from components.schemas.ShopUnit import ShopUnit
from components.schemas.ShopUnitType import ShopUnitType
from components.schemas.ShopUnitStatistic import ShopUnitStatistic
from components.schemas.ShopUnitImportRequest import ShopUnitImportRequest
from flask import request
from my_logs.logg import info_log, warning_log
from .base_function import delete_child, response_error_400, TIME_FORMAT
from flask import Blueprint


bp_imports = Blueprint('imports', __name__)




def valid_request_json(data: dict, time_format: str) -> bool:
    '''
        Проверка форматы даты и основной структуры
    '''

    if 'items' not in data or 'updateDate' not in data or len(data) != 2:
        info_log.warning('POST:/imports Проблемы с общей структурой входных данных')
        warning_log.warning(
            f'POST:/imports Проблемы с общей структурой входных данных:\ndata={data}\n, 400')
        return False

    try:
        datetime.datetime.strptime(data['updateDate'], time_format)
        return True
    except ValueError:
        info_log.warning(f'POST:/imports Проблемы с форматом даты')
        warning_log.warning(
            f'POST:/imports Проблемы  с форматом даты:\ndata={data}\n, 400')
        return False


def is_category(node_id: object) -> bool:
    if node_id is None:
        return True
    node = ShopUnit.query.filter_by(id=node_id).first()
    if node is not None:
        category = node.type
        return category == 'CATEGORY'
    return True


def valid_structure_item(item: dict) -> bool:
    '''
        Проверяем все ли необходимые параметры нам передали.
    '''
    if item['type'] in ['CATEGORY', 'OFFER']:
        if all(key in item for key in ['id', 'name', 'type']) and item['name'] is not None:
            return True
    info_log.warning('POST:/imports Проблемы с отдельной структурой item')
    warning_log.warning(
        f'POST:/imports Проблемы с отдельной структурой item:\nitem={item}\n, 400')
    return False


def valid_item(item: dict) -> bool:
    '''
        Проверка: Дочерние эл-ты могут быть только у CATEGORY
    '''
    parent_id = value_or_none(dict_=item, key_='parentId')
    price = value_or_none(dict_=item, key_='price')
    if not is_category(parent_id):
        info_log.warning(f'POST:/imports родителем может быть только категория')
        warning_log.warning(
            f'POST:/imports Проблемы с отдельной структурой item (parent_id) :\nitem={item}\n, 400')
        return False
    if price is not None and price < 0:
        info_log.warning(f'POST:/imports цена должна быть больше 0')
        warning_log.warning(
            f'POST:/imports Проблемы с отдельной структурой item (price) :\nitem={item}\n, 400')
        return False
    return True


def value_or_none(dict_: dict, key_: str) -> object:
    if key_ in dict_:
        return dict_[key_]
    return None


def add_child(id_child: str, id_parent: object) -> None:
    '''
        У узла id_parent появился дочерний эл-т id_child
    '''
    parent = ShopUnit.query.filter_by(id=id_parent).first()
    if id_child != id_parent: # проверяем на циклы
        if parent is not None: # если это корень, то пропускаем шаг
            if parent.children is not None:
                parent.children = set(list(parent.children) + [id_child])
            else:
                parent.children = [id_child]


def check_type_context(type: str, price: object) -> bool:
    '''
        Проверка параметров, зависящих от типа
    '''
    if type == 'CATEGORY':
        if price is not None:
            info_log.warning(
                f'POST:/imports В 1 запросе не может быть дубликатов type={type} price!={price}, 400', )
            return False
    if type == 'OFFER':
        if price is None or price < 0:
            info_log.warning(
                f'POST:/imports В 1 запросе не может быть дубликатов type={type} price!={price}, 400', )
            return False

    return True


def save_statistic(node_id: str, parentId: object, name: str, type_: str, price: object, time_: datetime) -> None:
    '''
        Фиксируем любое изменение для статистики
    '''

    problem = ShopUnitStatistic.query.filter_by(id=node_id).filter_by(date=time_).first()
    if problem is None:
        new_node = ShopUnitStatistic(id=node_id, name=name, date=time_, type=type_)
        new_node.parentId = parentId
        new_node.price = price
        db.session.add(new_node)
    else:
        info_log.info('поле updateDate монотонно возрастает по условию')


def add_node(node_id: str, parentId: object, name: str, type_: str, price: object, time_: datetime) -> None:
    '''
        Функция добавления новой записи по id
    '''
    new_node = ShopUnit(id=node_id, name=name, date=time_, type=type_)
    new_node.parentId = parentId
    add_child(id_child=node_id, id_parent=parentId)
    new_node.price = price
    if type_ == 'CATEGORY':
        new_node.children = []
    db.session.add(new_node)

    save_import_fact(node_id, name, parentId, type_, price)
    save_statistic(node_id, parentId, name, type_, price, time_)

    info_log.info(f'POST:/imports Новый обьект id={node_id}, 200')




def update_date_parent(node_id: object, time_update: datetime) -> None:
    '''
        Функция обновления даты по id родителя
    '''
    if node_id is None:
        return
    node = ShopUnit.query.filter_by(id=node_id).first()
    if node is not None:
        node.date = time_update
        db.session.add(node)
        save_statistic(node_id=node.id, parentId=node.parentId, name=node.name, type_=node.type, price=node.price,
                       time_=time_update)
        update_date_parent(node_id=node.parentId, time_update=time_update)


def save_import_fact(node_id: str, name: str, parentId: object, type: str, price: object) -> None:
    '''
        Фиксируем факт импорта
    '''
    unit_import = ShopUnitImport.query.filter_by(id=node_id).first()
    if unit_import is None:
        unit_import = ShopUnitImport(id=node_id, name=name, type=type)
    unit_import.name = name
    unit_import.parentId = parentId
    unit_import.type = type
    unit_import.price = price
    db.session.add(unit_import)


def save_request_fact(ids: set, update_date: datetime):
    '''
        Фиксируем факт отправки
    '''
    new_import_request = ShopUnitImportRequest()
    new_import_request.items = list(ids)
    new_import_request.updateDate = update_date
    db.session.add(new_import_request)


def update_node(node_id: str, old_parentId: object, parentId: object, name: str, type_: str, price: object,
                time_: datetime) -> None:
    '''
        Обновление значений записи в бд по id
    '''
    node = ShopUnit.query.filter_by(id=node_id).first()
    node.parentId = parentId
    delete_child(id_child=node_id, id_parent=old_parentId) #удаляем ребенка у старого родителя
    add_child(id_child=node_id, id_parent=parentId) #добавляем ребенка новому родителю
    node.name = name
    node.type = type_
    node.price = price
    node.date = time_
    db.session.add(node)

    save_import_fact(node_id, name, parentId, type_, price)
    save_statistic(node_id, parentId, name, type_, price, time_)

    info_log.info(
        f'POST:/imports Обновление обьекта id={node_id} name={name}, price={price}, date={time_} ch={node.children}, 200')



def id_duplicate(ids: set, new_id: str) -> bool:
    '''
            Проверка на наличие дубликатов id.
            ids - множество всех id в текущем запросе
    '''
    if new_id not in ids:
        ids.add(new_id)
        return False
    info_log.warning(
        f'POST:/imports В 1 запросе не может быть дубликатов id={ids} + {new_id}, 400', )
    return True


def main_handler_item(item: dict, update_date: datetime) -> int:
    '''
        Основная функция обработки валидной item и валидной update_date
    '''
    new_parent_id = value_or_none(dict_=item, key_='parentId')
    new_price = value_or_none(dict_=item, key_='price')

    node = ShopUnit.query.filter_by(id=item['id']).first()
    type_obj = ShopUnitType.query.filter_by(type=item['type']).first()
    new_type = type_obj.type

    if not check_type_context(type_obj.type, new_price):
        return response_error_400()

    if node is not None:
        # Если уже есть в базе такой id, значения нужно обновить запись
        if node.type != new_type:
            return 400
        old_parent_id = node.parentId
        update_node(node_id=item['id'], parentId=new_parent_id, name=item['name'],
                    type_=new_type, price=new_price, time_=update_date, old_parentId=old_parent_id, )
        if old_parent_id is not None:
            #обновляем старого родителя (время)
            update_date_parent(old_parent_id, time_update=update_date)
    else:
        # иначе создаем новую запись
        add_node(node_id=item['id'], parentId=new_parent_id, name=item['name'], type_=new_type,
                 price=new_price, time_=update_date)

    if new_parent_id is not None:
        # обновляем нового родителя (время)
        update_date_parent(new_parent_id, time_update=update_date)
    return 200


@bp_imports.route('/imports', methods=['POST'])
def imports():
    '''
        Обработчик для импортирования новых товаров и/или категорий.
    '''

    info_log.info('handler:POST:/imports ')
    if not request.is_json:
        info_log.warning(f'handler:POST:/imports это не json')
        return response_error_400()

    data = request.get_json()

    if not valid_request_json(data, TIME_FORMAT):
        return response_error_400()

    update_date = datetime.datetime.strptime(data['updateDate'], TIME_FORMAT)
    update_date = update_date.isoformat()

    ids = set()
    for item in data['items']:
        if (not valid_structure_item(item)) or (not valid_item(item)) or (id_duplicate(ids, item['id'])):
            return response_error_400()
        if main_handler_item(item=item, update_date=update_date) != 200:
            info_log.warning('handler:POST:/imports Нельзя менять типы')
            return response_error_400()

    save_request_fact(ids, update_date)
    db.session.commit()
    return '', 200
