# coding:utf-8
"""
使用缓存的csv文件补上数据库缺失数据
"""
import os
from datetime import datetime

import pandas.io.sql as psql

import csv
from db_utils import engine


def insert_rows(sql: str, rows: list):
    res = psql.execute(sql, engine, params=rows)
    effect_ct = res.rowcount
    if effect_ct:
        print('{} rows had been inserted to the hko.'.format(res.rowcount))


def gen_rows(path: str):
    print('walking through:', path)
    count = 0
    for root, dirs, files in os.walk(path):
        for f_name in files:
            if f_name.endswith('.csv'):
                # stdout.write(f'\r{f_name}')
                # stdout.flush()
                with open(os.path.join(root, f_name)) as fp:
                    reader = csv.reader(fp)
                    yield list(reader)
            count += 1
        print(f'{count} files have been checked.')
        break


def fix_hko(f_path):
    print(datetime.now())
    for rows in gen_rows(f_path):
        for row in rows:
            if len(row) != 14:
                print('数据存在问题', row)
                continue
            row.extend((row[0], row[1]))
        sql = """
        insert into hko (pub_time, STN, WINDDIRECTION, WINDSPEED, GUST, TEMP, RH, MAXTEMP, MINTEMP, GRASSTEMP, 
        GRASSMINTEMP, VISIBILITY, PRESSURE, TEMPDIFFERENCE) 
        select %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s from dual
        where not exists
        (select 1 from hko where pub_time=%s and STN=%s)
        """
        insert_rows(sql, rows)
    print(datetime.now())


def fix_pollutant(f_path):
    print(datetime.now())
    for rows in gen_rows(f_path):
        rows = rows[1:]
        for row in rows:
            if len(row) != 9:
                print('数据存在问题', row)
                continue
            row.extend((row[0], row[-2]))
        sql = """
        insert into pollutant (pub_time, NO2, O3, SO2, CO, PM10, `PM2.5`, station_id, station_name) 
        select %s, %s, %s, %s, %s, %s, %s, %s, %s from dual
        where not exists
        (select 1 from pollutant where pub_time=%s and station_id=%s)
        """
        insert_rows(sql, rows)
    print(datetime.now())


if __name__ == '__main__':
    fix_hko('csv/hko')
    fix_pollutant('csv')
