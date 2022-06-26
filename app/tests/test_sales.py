from base_functions import *
from components.schemas.ShopUnit import ShopUnit
from my_logs.logg import info_log


def date_format(date_str):
    return datetime.datetime.strptime(date_str, TIME_FORMAT)


def test_sales(day_str, day_datetime):
    params = urllib.parse.urlencode({
        "date": day_str
    })
    status, response = request(f"/sales?{params}", json_response=True)
    assert status == 200, f"Expected HTTP status code 200, got {status}"
    ids = set()
    for item in response['items']:
        ids.add(item['id'])
        assert item['type'] == 'OFFER'
        assert day_datetime - datetime.timedelta(days=1) <= date_format(item['date']) <= day_datetime
    ids_real = set()
    for node in ShopUnit.query.all():
        if node.type == 'OFFER':
            if day_datetime - datetime.timedelta(days=1) <= date_format(
                    node.date.isoformat() + '.000Z') <= day_datetime:
                ids_real.add(node.id)
    assert ids_real == ids, f't=[{day_datetime - datetime.timedelta(days=1)}; {day_datetime} правильно={ids_real}, сейчаc={ids}, \nurl=/sales?{params}'


def test_valid_date(logger, n=1):
    '''
        Проверка обновленных таваров во времени.
        Идея: Генерация случайного дерева, потом проверить ответ и значения в бд (все ли значения передали)

    '''
    logger.info('stat test_valid_date: start')
    for x in range(n):
        tree, last_id_category, last_id_offer, date_first, date_end = create_random_tree()

        import_tree(logger, tree)

        date_first = date_first - datetime.timedelta(days=random.randint(5, 10))
        date_end = date_end + datetime.timedelta(days=random.randint(5, 10))
        while date_first < date_end:
            date_first = date_first + datetime.timedelta(days=1)

            day = date_first.strftime(TIME_FORMAT)

            for id_offer in range(last_id_offer + 1, last_id_category, 1):
                if id_offer == 0:
                    continue
                test_sales(day_str=day, day_datetime=date_first)
    logger.info('stat test_valid_date: passed')


if __name__ == '__main__':
    logger = info_log
    test_valid_date(logger)
