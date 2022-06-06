import traceback
import uuid
from collections import defaultdict
import datetime

import requests
from requests.packages import urllib3
import pandas.io.sql as psql

from db_utils import engine
from mail import send_mail
from utils import retry

urllib3.disable_warnings()


@retry()
def run(uid: str = ''):
    uid = uid or uuid.uuid4()
    ts_url = f"https://www.haze.gov.sg/api/UnixTime/GetTime/{uid}"
    ts = requests.get(ts_url, verify=False).text

    json_url = f"https://www.haze.gov.sg/api/airquality/jsondata/{ts}"
    res = requests.get(json_url, verify=False).json()

    data = defaultdict(list)
    for pollutant, ptype in zip(['Chart1HRPM25', 'ChartPM10', 'ChartSO2', 'ChartO3', 'ChartCO', 'ChartNO2'],
                                ['PM25', 'PM10', 'SO2', 'O3', 'CO', 'NO2']):
        for location in ['North', 'South', 'East', 'West', 'Central']:
            for d in res[pollutant][location]['Data']:
                val, dt = d['value'], d['dateTime']
                dt = datetime.datetime.strptime(dt, '%d %b %Y %I%p')
                data[(location, dt)].append([ptype, val])
    # [location, dt, 'PM25', 'PM10', 'SO2', 'O3', 'CO', 'NO2']
    # ['North', datetime.datetime(2022, 6, 2, 14, 0), 15.0, 33.0, 4.0, 8.0, 5.0, 0.0]
    rows = [[*k, *(i[1] for i in v)] for k, v in data.items()]
    # for row in rows:
    #     row.extend(row[-6:])
    sql = """
    insert into sg_pollutant (STN, PUB_TIME, PM25, PM10, SO2, O3, CO, NO2) 
    values(%s, %s, %s, %s, %s, %s, %s, %s)
    on duplicate key update 
    PM25=values(PM25), PM10=values(PM10), SO2=values(SO2), O3=values(O3), CO=values(CO), NO2=values(NO2)    
    """
    res = psql.execute(sql, engine, params=rows)
    print('{}/{} rows had been inserted to the sg_pollutant. \n{}\n'.format(res.rowcount, len(rows),
                                                                            datetime.datetime.now()))


if __name__ == '__main__':
    try:
        run()
    except Exception:
        subject = 'sg-pollutant数据获取出错'
        content = traceback.format_exc()
        send_mail(
            mail_subject=subject,
            mail_content=content
        )
