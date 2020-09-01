# coding:utf-8
import csv
import os
import traceback
from datetime import datetime

import pandas.io.sql as psql
from pyquery import PyQuery as pq

from db_utils import engine
from mail import send_mail
from utils import retry


@retry()
def run():
    print(datetime.now())
    url = 'https://maps.weather.gov.hk/r4/input_files/latestReadings_AWS1'
    e = pq(url=url)
    weather_list = e[0].text_content().rstrip('\n').split('\n')
    # 'Latest readings recorded at 13:30 Hong Kong Time 15 May 2020'
    release_str = weather_list[0].split(' at ')[1]
    try:
        release_date = datetime.strptime(release_str, '%H:%M Hong Kong Time %d %b %Y')
    except ValueError:
        date_list = release_str.split(' ')
        date_list[-2] = datetime.now().strftime('%b')
        release_str = ' '.join(date_list)
        release_date = datetime.strptime(release_str, '%H:%M Hong Kong Time %d %b %Y')

    data = []
    # columns = ['STN', 'WINDDIRECTION', 'WINDSPEED', 'GUST', 'TEMP', 'RH', 'MAXTEMP',
    #            'MINTEMP', 'GRASSTEMP', 'GRASSMINTEMP', 'VISIBILITY', 'PRESSURE', 'TEMPDIFFERENCE']

    for w in weather_list[2:]:
        row = [release_date] + [i if i else None for i in w.split(',')[:-1]]
        if len(row) == 14:
            data.append(row)
        else:
            # STN CP1数据有时会有15列，单独写到文件中
            with open('cp1.csv', 'a') as f:
                f.write(','.join(map(str, row))+'\n')
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
    print('{}/{} rows had been inserted to the hko. \n{}\n'.format(res.rowcount, len(data), datetime.now()))


if __name__ == '__main__':
    try:
        run()
    except Exception:
        subject = 'hko数据获取出错'
        content = traceback.format_exc()
        send_mail(
            # mail_from='爬虫SERVER',
            mail_subject=subject,
            mail_content=content
        )
