# coding:utf-8
import csv
import os
from datetime import datetime

import pandas.io.sql as psql
from pyquery import PyQuery as pq

from db_utils import engine

url = 'https://maps.weather.gov.hk/r4/input_files/latestReadings_AWS1'
e = pq(url=url)
weather_list = e[0].text_content().rstrip('\n').split('\n')
# 'Latest readings recorded at 13:30 Hong Kong Time 15 May 2020'
release_str = weather_list[0].split(' at ')[1]
release_date = datetime.strptime(release_str, '%H:%M Hong Kong Time %d %b %Y')

data = []
columns = ['STN', 'WINDDIRECTION', 'WINDSPEED', 'GUST', 'TEMP', 'RH', 'MAXTEMP', 'MINTEMP', 'GRASSTEMP', 'GRASSMINTEMP',
           'VISIBILITY', 'PRESSURE', 'TEMPDIFFERENCE']

for w in weather_list[2:]:
    row = [release_date] + [i if i else None for i in w.split(',')[:-1]]
    print(len(row))
    data.append(row)

csv_file_name = 'hko{}.csv'.format(release_date.strftime('%Y%m%d%H%M%S'))
if not os.path.exists('csv/hko'):
    os.mkdir('csv/hko')

# 写入数据库前, 保存csv文件备份
csv_writer = csv.writer(open(os.path.join('csv/hko', csv_file_name), 'w'))
csv_writer.writerows(data)
print('成功保存csv文件,', csv_file_name)

for row in data:
    row.extend((row[0], row[1]))
sql = """
insert into hko (pub_time, STN, WINDDIRECTION, WINDSPEED, GUST, TEMP, RH, MAXTEMP, MINTEMP, GRASSTEMP, 
GRASSMINTEMP, VISIBILITY, PRESSURE, TEMPDIFFERENCE) 
select %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s from dual
where not exists
(select 1 from hko where pub_time=%s and STN=%s)
"""
res = psql.execute(sql, engine, params=data)
print('{} rows had been inserted to the hko. \n{}\n'.format(len(data), datetime.now()), res.rowcount)
