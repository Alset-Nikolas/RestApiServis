# RestApiServis
Пояснение к структуре:

    app ->   Python-пакет с проектом
     |-- components   (БД)
     |      | -- schemas -> пакет с описаниями схем БД
     |      |       | -- __init__.py 
     |      |       | -- Error.py  -> схема Error
     |      |       | -- ShopUnit.py -> схема ShopUnit
     |      |       | -- ShopUnitImport.py -> схема ShopUnitImport
     |      |       | -- ShopUnitImportRequest.py -> схема ShopUnitImportRequest
     |      |       | -- ShopUnitStatisticResponse.py -> схема ShopUnitStatisticResponse
     |      |       | -- ShopUnitStatisticUnit.py -> схема ShopUnitStatisticUnit
     |      |       | -- ShopUnitType.py -> схема ShopUnitType
     |      | -- __init__ -> Суть: заполнить app.config
     |-- my_logs  (Логирование)
     |      | -- logg.py -> Кофигурация логера
     |      | -- __init__.py
     |-- paths  (URL)
     |      | -- base_function.py -> Общие функции в рамках paths
     |      | -- delete.py -> Обработчик удаления элемента по идентификатору. /delete/<id_>
     |      | -- imports.py -> Обработчик для импортирования новых товаров и/или категорий. /imports
     |      | -- node_id.py -> Обработчик по выводу информации по id '/nodes/<id_>'
     |      | -- sales.py -> Получение списка **товаров** в интервале времени  /sales
     |      | -- statistic.py  -> Получение статистики по товару/категории за заданный полуинтервал /node/<id_>/statistic
     |      | -- __init__.py
     |-- tests  (Тесты)
     |      | -- base_function.py -> Общие функции в рамках tests
     |      | -- test_delete.py -> Тесты /delete/<id_>
     |      | -- test_imports.py -> Тесты /imports
     |      | -- test_node_id.py -> Тесты '/nodes/<id_>'
     |      | -- test_sales.py -> Тесты  /sales
     |      | -- test_statistic.py  -> Тесты /node/<id_>/statistic 
     |      | -- unit_test.py -> Тесты (изначальные тесты)
     |      | -- __init__.py
    migrations ->   Миграции
     |      
        ...   ->   файлы миграции
     |      
    main.py ->   файл запуска app
     |      
    openapi.yaml  -> Задание (1)
     |   
    README.md -> Этот файл :)
     |
    requirements.txt -> файл зависимостей
     |
    Task.md -> Задание (2)
