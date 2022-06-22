from base_functions import *
import test_delete
import test_import
import test_node_id
from unit_test import main

logger = create_logging()
test_delete.test_all(logger)
test_import.test_all(logger)
test_node_id.test_all(logger)
main(logger)