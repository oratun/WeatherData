import datetime

import pymysql

from settings import db_config

# config = {
#     'user': 'username',
#     'password': 'pwd',
#     'host': 'ip',
#     'port': 3306,
#     'database': 'test'
# }

connection = pymysql.connect(**db_config,
                             charset='utf8mb4',
                             autocommit=True,
                             )


def execute_many(table: str, sql: str, rows: list) -> int:
    with connection.cursor() as cursor:
        row_count = cursor.executemany(sql, rows)
        print(f'{row_count}/{len(rows)} rows had been inserted to the {table}. \n{datetime.datetime.now()}\n')
        return row_count
