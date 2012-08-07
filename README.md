rest-tester
===========

Python скрипт для тестирования cmios REST API (http://cmios.ru/development/apiv2/).

Установка
---------

Скрипт требует установленного интерпретатора python. В большинстве современных unix систем он уже установлен.
Для Windows инсталлятор можно скачать с официального сайта http://python.org/download/

Использование
-------------

python cmios_rest_tester.py [-e EMAIL] [-s SECRET] [-H HOST] [-p PREFIX] [-m {GET,POST,PUT}] [-j JSON] url

* -h, --help    эта помощь
*  -e EMAIL, --email EMAIL email пользователя
* -s SECRET, --secret SECRET пароль групповой авторизации
* -H HOST, --host HOST  адрес сайта для тестирования (необязательно)
*  -p PREFIX, --prefix PREFIX префикс API url
* -m {GET,POST,PUT}, --method {GET,POST,PUT} метод запроса
* -j JSON, --json JSON  json файл с параметрами запроса
* URL - url запроса

Примеры
-------

* `python cmios_rest_tester.py car_mark` - список марок автомобилей
* `python cmios_rest_tester.py calculation/list` - список расчётов
* `python cmios_rest_tester.py --method POST --json calculation_simple.json calculation` - создание расчёта

