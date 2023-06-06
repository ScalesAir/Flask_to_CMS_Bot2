import asyncpg
import asyncio
from logs import logging
from config.config import db_user, db_password, db_host, db_port, db_database

lock = asyncio.Lock()

__all__ = [
    'sql_start',
    'read_requests',
    'read_activ_requests',
    'sql_close',
]

logger = logging.getLogger("app.data_base.pg_bd")

base: asyncpg.pool.Pool  # Определяем тип глобальной переменной base


async def sql_start():
    """
    Данная функция выполняется при запуске бота.
    И создает таблицы в БД если они не созданы.
    (Если таблица создана, но в этом коде добавлено новое поле, оно не будет добавлено. Его необходимо добавить в БД
    самим, или удалить таблицу из БД и перезапустить бота)
    :return:
    """
    global base
    try:
        # Подключение к существующей базе данных
        base = await asyncpg.create_pool(user=db_user,
                                         password=db_password,
                                         host=db_host,
                                         port=db_port,
                                         database=db_database)

        if base:
            logger.info(f'БД подключена')
        else:
            logger.info(f'БД не подключилась')
    except Exception as err_bd:
        logger.critical(err_bd)


# async def sql_read(tabl):
#     temp = await base.fetch(f'''
#                     SELECT tb_requests.*, u1.name AS user_name, u2.name AS specialist_name
#                     FROM {tabl} AS tb_requests
#                     LEFT JOIN tb_users AS u1 ON tb_requests.user_id = u1.telegram_id
#                     LEFT JOIN tb_users AS u2 ON tb_requests.specialist_id = u2.telegram_id
#                     ORDER BY 1
#                 ''')
#     return list(temp)


async def read_requests():
    temp = await base.fetch(f'''
                    SELECT tb_requests.*, 
                    u1.name AS user_name, u1.region AS user_region, u2.name AS specialist_name, tb_regions.region
                    FROM tb_requests AS tb_requests
                    LEFT JOIN tb_users AS u1 ON tb_requests.user_id = u1.telegram_id
                    LEFT JOIN tb_users AS u2 ON tb_requests.specialist_id = u2.telegram_id
                    LEFT JOIN tb_regions ON u1.region = tb_regions.region_id
                    ORDER BY 1
                ''')
    return list(temp)


async def read_activ_requests():
    return await base.fetch('SELECT * FROM tb_active_requests ORDER BY request_id')


async def sql_close():
    """
    Закрывает БД.
    :return:
    """
    await base.close()
    logger.info('БД закрыта')
