import datetime
import random

from base_functions import *
from components.schemas.ShopUnitStatistic import ShopUnitStatistic

time_format = "%Y-%m-%dT%H:%M:%S.%f%z"


def clear_history():
    for node in ShopUnitStatistic.query.all():
        db.session.delete(node)
    db.session.commit()
    assert len(ShopUnitStatistic.query.all()) == 0


def import_history(data_first="2022-02-01T12:00:00.000Z", days=10):
    for i, price in enumerate(range(10)):
        date = datetime.datetime.strptime(data_first, time_format) + datetime.timedelta(days=i)

        tree_i = {
            "items": [
                {
                    "type": "CATEGORY",
                    "name": f"Смартфоны {i}",
                    "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
                },
                {
                    "type": "OFFER",
                    "name": "jPhone 13",
                    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": price
                },
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 2 * price + 1
                }
            ],
            "updateDate": str(date.strftime(time_format))[:-8] + 'Z'
        }

        status, x = request("/imports", method="POST", data=tree_i)
        assert status == 200, f"Expected HTTP status code 200, got {status}"


def import_tree(tree):
    for tree_i in tree:
        status, x = request("/imports", method="POST", data=tree_i)
        assert status == 200, f"Expected HTTP status code 200, got {status}"


def test_stats(id, start_t=None, end_t=None):
    params_dict = dict()
    flags = [0, 0]
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
    for item in response:
        date_item = item['date']
        if flags[0]:
            assert date_format(params_dict['dateStart']) <= date_format(
                date_item), f'time={date_format(date_item)} t=>{date_format(params_dict["dateStart"])}'
        if flags[1]:
            assert date_format(date_item) < date_format(
                params_dict['dateEnd']), f'time={date_format(date_item)} t<{date_format(params_dict["dateEnd"])} )'

    return response


def date_format(date_str):
    return datetime.datetime.strptime(date_str, time_format)



def test_valid_date():
    for x in range(10):
        # clear_history()
        # tree, last_id_category, last_id_offer, date_first, date_end = create_random_tree()
        #
        # import_tree(tree)

        date_first = date_first + datetime.timedelta(days=random.randint(-5, 5))
        date_end = date_end + datetime.timedelta(days=random.randint(-5, 5))
        while date_first > date_end:
            date_first = date_first + datetime.timedelta(days=random.randint(-5, 5))
            date_end = date_end + datetime.timedelta(days=random.randint(-5, 5))

        start_day = str(date_first.strftime(time_format))[:-8] + 'Z'
        date_end = str(date_end.strftime(time_format))[:-8] + 'Z'

        for id_offer in range(-1, last_id_offer, -1):
            test_stats(id=str(id_offer) + '-10000', start_t=start_day, end_t=date_end)

if __name__ == '__main__':
    logger = create_logging()
    # clear_history()
    # import_history()
    test_valid_date()


