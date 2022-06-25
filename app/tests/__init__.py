from base_functions import *
import test_delete
import test_import
import test_node_id
from unit_test import main
import test_static


def test_run():
    logger = create_logging()
    clear_bd(logger)
    test_delete.test_all(logger)
    test_import.test_all(logger)
    test_node_id.test_all(logger)
    main(logger)
    test_static.test_valid_date(logger)
    clear_bd(logger)


if __name__ == '__main__':
    test_run()
