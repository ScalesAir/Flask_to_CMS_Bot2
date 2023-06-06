import os
import configparser  # импортируем библиотеку для работы с .ini

current_dir = os.getcwd()
config = configparser.ConfigParser()  # создаём объекта парсера .ini
config.read(f"{current_dir}/settings.ini", encoding="utf-8")  # читаем конфиг

db_user = config["DB"]["user"]
db_password = config["DB"]["password"]
db_host = config["DB"]["host"]
db_port = config["DB"]["port"]
db_database = config["DB"]["database"]
app_host = config["APP"]["host"]
origins = config["APP"]["origins"]
