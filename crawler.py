# coding:utf-8
import os
import traceback
from datetime import datetime

import pandas as pd
import pandas.io.sql as psql
from pandas import DataFrame as df
from pyquery import PyQuery as pq

from db_utils import engine
from mail import send_mail
from utils import retry


@retry()
def run():
    print(datetime.now())
    base_url = 'http://www.aqhi.gov.hk/sc/aqhi/'
    url = 'http://www.aqhi.gov.hk/sc/aqhi/past-24-hours-pollutant-concentration.html'
    e = pq(url=url)
    station_item_list = e('.stationList_item_a')

    # {'中西区': 'past-24-hours-pollutant-concentration45fd.html?stationid=80', }
    station_dict = {station.text: station.attrib['href'] for station in station_item_list}

    data = pd.DataFrame()
    columns = ['日期时间', '二氧化氮', '臭氧', '二氧化硫', '一氧化碳', 'PM10', 'PM2.5']

    for name, url in station_dict.items():
        info_list = pd.read_html(base_url + url, parse_dates=True)
        d = df().append(info_list).reset_index().loc[1:, columns]
        d['station_id'] = int(url[-2:])
        d['station_name'] = name
        d.replace(['-'], [None], inplace=True)

        d['日期时间'] = d['日期时间'].str.replace('\xa0', ' ')
        d['日期时间'] = pd.to_datetime(d['日期时间'], )
        # d['日期时间'] = d['日期时间'].to_timestamp()
        data = data.append(d, ignore_index=True)
        # break

    csv_file_name = 'pollutant{}.csv'.format(datetime.now().strftime('%Y%m%d%H%M%S'))
    if not os.path.exists('csv'):
        os.mkdir('csv')

    # 写入数据库前, 保存csv文件备份
    data.to_csv(os.path.join('csv', csv_file_name), index=False)
    # data.to_sql('pollutant', con=engine, if_exists='append', index=False, method='multi')
    print('成功保存csv文件,', csv_file_name)

    row_list = data.values.tolist()
    for row in row_list:
        row[0] = row[0].to_pydatetime()
        row.extend((row[0], row[-2]))

    sql = """
    insert into pollutant (pub_time, NO2, O3, SO2, CO, PM10, `PM2.5`, station_id, station_name) 
    select %s, %s, %s, %s, %s, %s, %s, %s, %s from dual
    where not exists
    (select 1 from pollutant where pub_time=%s and station_id=%s)
    """
    res = psql.execute(sql, engine, params=row_list)
    print('{} rows had been inserted to the db. \n{}\n'.format(len(row_list), datetime.now()), res.rowcount)


if __name__ == '__main__':
    try:
        run()
    except Exception:
        subject = 'pollutant数据获取出错'
        content = traceback.format_exc()
        send_mail(
            # mail_from='爬虫SERVER',
            mail_subject=subject,
            mail_content=content
        )
