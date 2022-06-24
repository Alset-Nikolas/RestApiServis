# RestApiServis - Задание от Яндекс Школа бэкенд-разработки 2022г

# Для запуска
1. Заходим на сервер или локальную машину
2. Клонируем репозиторий https://github.com/Alset-Nikolas/RestApiServis
3. Затем нужно забилдить и поднять контейнер с помощью Docker Compose в этом помогут команды ниже
   - sudo docker-compose -f docker-compose.dev.yml build # Билд
   - sudo docker-compose -f docker-compose.dev.yml up # Запуск
   - sudo docker-compose -f docker-compose.dev.yml up -d # Запуск в фоне
   - sudo docker-compose -f docker-compose.dev.yml stop # Остановка
4. Нужно создать таблицы бд
   - sudo docker exec flask_azz_yt flask  commands create_db

# Пояснение к структуре проекта:

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
     |      | -- __init__ 
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
     | -- config.py ->   файл кофигурации
     | -- consol.py ->   файл запуска create_bd в консоли
     | -- db.py ->   вынесено в отдельный файл для декомпозиции моделей
     | -- Dockerfile ->   Dockerfile
     | -- main.py ->   файл запуска app
     | -- main.py ->   requirements.txt -> файл зависимостей
    migrations ->   Миграции
     |      
        ...   ->   файлы миграции
     |      
    Task -> Папка Заданий
     |      
        ...   ->   файлы заданий
     |   
    docker-compose.yaml  -> docker-compose
     |   
    README.md -> Этот файл :)

