import datetime
from base_functions import *
time_format = "%Y-%m-%dT%H:%M:%S.%f%z"

def clear_history(logger):
    for node in ShopUnitStatisticUnit.query.all():
        db.session.delete(node)
    db.session.commit()
    assert len(ShopUnitStatisticUnit.query.all()) == 0



def import_history(logger=None, data_first="2022-02-01T12:00:00.000Z", days=10):
    for i, price in enumerate(range(10)):
        date = datetime.datetime.strptime(data_first, time_format) + datetime.timedelta(days=i)

        tree_i = {
            "items": [
                 {
                     "type": "CATEGORY",
                     "name": "Смартфоны",
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
                    "price": 2*price+1
                }
            ],
                 "updateDate": str(date.strftime(time_format))[:-8] + 'Z'
        }

        status, x = request("/imports", method="POST", data=tree_i)
        assert status == 200, f"Expected HTTP status code 200, got {status}"


def test_stats(id, start_t, end_t):
    # params = urllib.parse.urlencode({
    #     "dateStart": "2022-02-01T00:00:00.000Z",
    #     "dateEnd": "2022-02-03T00:00:00.000Z"
    # })
    params = urllib.parse.urlencode({
        "dateStart": start_t,
        "dateEnd": end_t
    })
    status, response = request(
        f"/node/{id}/statistic?{params}")

    assert status == 200, f"Expected HTTP status code 200, got {status}"
    return response

def check_valid_date(logger):
    data_first = '2022-02-01T12:00:00.000Z'
    days = 20
    clear_history(logger)
    import_history(logger, data_first, days)
    re=test_stats(id='d515e43f-f3f6-4471-bb77-6b455017a2d2', start_t="2022-01-03T00:00:00.000Z", end_t="2022-02-03T00:00:00.000Z")

if __name__ == '__main__':
    logger = create_logging()
    clear_history(logger)
    import_history(logger)
    re=test_stats(id='d515e43f-f3f6-4471-bb77-6b455017a2d2', start_t="2022-01-03T00:00:00.000Z", end_t="2022-02-03T00:00:00.000Z")
    print(re)