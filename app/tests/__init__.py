from . import test_delete, test_node_id, test_static, test_import
from .unit_test import main
from my_logs.logg import info_log
from .test_sales import test_valid_date
from .base_functions import clear_bd, clear_bd_after_tests

def test_run(logger):
    '''
        Основные тесты
    '''
    clear_bd(logger)
    test_delete.test_all(logger)
    test_import.test_all(logger)
    test_node_id.test_all(logger)
    main(logger)
    clear_bd_after_tests()

def long_test_run(logger):
    '''
        Более глубокий анализ, создается случайное дерево
    '''
    test_import.test_import_random_tree(logger)
    test_delete.test_delete_random_tree(logger)
    test_node_id.test_node_id_random_tree(logger)
    test_static.test_valid_date(logger)
    test_valid_date(logger)


if __name__ == '__main__':
    test_run(info_log)
    long_test_run(info_log)
    clear_bd_after_tests()
