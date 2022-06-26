import datetime
import random
from my_logs.logg import info_log
from base_functions import *
from components.schemas.ShopUnitStatistic import ShopUnitStatistic


def test_stats(id, start_t=None, end_t=None):
    params_dict = dict()
    flags = [False, False]
    if start_t:
        params_dict['dateStart'] = start_t
        flags[0] = True
    if end_t:
        params_dict['dateEnd'] = end_t
        flags[1] = True
    params = urllib.parse.urlencode(params_dict)
    status, response = request(
        f"/node/{id}/statistic?{params}", json_response=True)

    assert status == 200, f"Expected HTTP status code 200, got {status}"
    ids = set()

    for item in response['items']:
        date_item = str(item['date'])[:-6] + '0.000000+0000'
        ids.add((item["id"], item["date"]))
        if flags[0]:
            assert date_format(params_dict['dateStart']) <= date_format(
                date_item), f'time={date_format(date_item)} t=>{date_format(params_dict["dateStart"])}'
        if flags[1]:
            assert date_format(date_item) < date_format(
                params_dict['dateEnd']), f'time={date_format(date_item)} t<{date_format(params_dict["dateEnd"])} )'

    ids_real = set()
    for node in ShopUnitStatistic.query.filter_by(id=id).all():
        if flags[0] and not flags[1]:

            if date_format(params_dict['dateStart']) <= date_format(node.date.isoformat() + '.000Z'):
                ids_real.add((node.id, node.date.isoformat() + '.000Z'))
        if flags[1] and not flags[0]:

            if date_format(node.date.isoformat() + '.000Z') < date_format(params_dict['dateEnd']):
                ids_real.add((node.id, node.date.isoformat() + '.000Z'))
        elif all(flags):

            if date_format(params_dict['dateStart']) <= date_format(node.date.isoformat() + '.000Z') < date_format(
                    params_dict['dateEnd']):
                ids_real.add((node.id, node.date.isoformat() + '.000Z'))
        else:
            ids_real.add((node.id, node.date.isoformat() + '.000Z'))
    assert ids == ids_real

    return response


def date_format(date_str):
    return datetime.datetime.strptime(date_str, TIME_FORMAT)


def test_valid_date(logger, n=1):
    '''Провереям '''
    logger.info('stat test_valid_date: start')
    for round_i in range(n):
        tree, last_id_category, last_id_offer, date_first, date_end = create_random_tree()

        import_tree(logger, tree)

        date_first = date_first + datetime.timedelta(days=random.randint(-5, 5))
        date_end = date_end + datetime.timedelta(days=random.randint(-5, 5))
        while date_first > date_end:
            date_first = date_first + datetime.timedelta(days=random.randint(-5, 5))
            date_end = date_end + datetime.timedelta(days=random.randint(-5, 5))

        start_day = date_first.strftime(TIME_FORMAT) if random.randint(1, 10) > 5 else None
        date_end = date_end.strftime(TIME_FORMAT) if random.randint(1, 10) > 5 else None

        for id_offer in range(last_id_offer + 1, last_id_category, 1):
            if id_offer == 0:
                continue
            test_stats(id=str(id_offer) + '-10000', start_t=start_day, end_t=date_end)
    logger.info('stat test_valid_date: passed')


if __name__ == '__main__':
    logger = info_log
    test_valid_date(logger)
