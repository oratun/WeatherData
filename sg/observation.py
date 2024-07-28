import datetime
import json
import logging
import re
import traceback
from collections import defaultdict
from urllib.parse import urlencode

import requests.exceptions
from pyquery import PyQuery as PQ

from db_utils import execute_many
from mail import send_mail

logger = logging.getLogger(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

stations = {'Paya Lebar': 'S06', 'Macritchie Reservoir': 'S07', 'Lower Peirce Reservoir': 'S08',
            'Jurong (North)': 'S101', 'Semakau Island': 'S102', 'Admiralty': 'S104', 'Admiralty West': 'S105',
            'Pulau Ubin': 'S106', 'East Coast Parkway': 'S107', 'Marina Barrage': 'S108', 'Ang Mo Kio': 'S109',
            'Choa Chu Kang (West)': 'S11', 'Serangoon North': 'S110', 'Newton': 'S111', 'Lim Chu Kang': 'S112',
            'Marine Parade': 'S113', 'Choa Chu Kang (Central)': 'S114', 'Tuas South': 'S115',
            'Pasir Panjang': 'S116', 'Jurong Island': 'S117', 'Dhoby Ghaut': 'S118', 'Nicoll Highway': 'S119',
            'Botanic Garden': 'S120', 'Choa Chu Kang (South)': 'S121', 'Khatib': 'S122', 'Whampoa': 'S123',
            'Tengah': 'S23', 'Changi': 'S24', 'Seletar': 'S25', 'Pasir Ris (West)': 'S29', 'Kampong Bahru': 'S31',
            'Jurong Pier': 'S33', 'Ulu Pandan': 'S35', 'Serangoon': 'S36', 'Jurong (East)': 'S39', 'Mandai': 'S40',
            'Tai Seng': 'S43', 'Jurong (West)': 'S44', 'Upper Thomson': 'S46', 'Clementi': 'S50', 'Buangkok': 'S55',
            'Sentosa Island': 'S60', 'Chai Chee': 'S61', 'Boon Lay (West)': 'S63', 'Bukit Panjang': 'S64',
            'Kranji Reservoir': 'S66', 'Upper Peirce Reservoir': 'S69', 'Kent Ridge': 'S71', 'Tanjong Pagar': 'S72',
            'Queenstown': 'S77', 'Tanjong Katong': 'S78', 'Somerset (Road)': 'S79', 'Sembawang': 'S80',
            'Punggol': 'S81', 'Tuas West': 'S82', 'Simei': 'S84', 'Boon Lay (East)': 'S86', 'Toa Payoh': 'S88',
            'Tuas': 'S89', 'Bukit Timah': 'S90', 'Yishun': 'S91', 'Buona Vista': 'S92',
            'Pasir Ris (Central)': 'S94'}


def run(hours=12):
    """
    因为不是所有的站点都有所有的数据, 所以需要分别爬取这几个页面，获得有该项数据的站点名称；
    从stations字典里取出stationCode，调用ajax接口获取该站点过去12/24/48小时数据。
    """
    page_url = 'https://www.weather.gov.sg/weather-currentobservations-{}/'
    keys = [
        'rainfall',
        'temperature', 'humidity', 'wind',
        'visibility'
    ]
    pattern = re.compile(r'.*<strong>(.*)</s')
    weather = defaultdict(dict)  # temp hr wind  {station: {pub_time: {'temp': temp, 'hr': hr, 'wind': wind}}}
    visibility = defaultdict(dict)

    for key in keys:
        url_key = 'relative-humidity' if key == 'humidity' else key
        url = page_url.format(url_key)
        e = PQ(url=url, headers=headers)
        if key == 'rainfall':
            pat = '.col-xs-2:gt(2):lt(9) li'
            for i in e(pat).items():
                station = i.text()
                get_station(url_key, station, hours, key, weather, visibility)
        else:
            for span in e('#sg_region_popover span'):
                # station = pattern.match(span.get('data-content')).group(1)
                station = span.get('id')
                get_station(url_key, station, hours, key, weather, visibility)
    if weather:
        rows = [(*k, *(v.get(i) for i in ['rainfall', 'temp', 'rh', 'windSpeedKpr', 'windDirection'])) for k, v in
                weather.items()]
        sql = """
        insert into sg_weather (STATION, PUB_TIME, RAINFALL, TEMP, RELATIVE_HUMIDITY, WIND_SPEED, WIND_DIRECTION) 
        values(%s, %s, %s, %s, %s, %s, %s)
        on duplicate key update RAINFALL=IFNULL(RAINFALL, values(RAINFALL)),
        TEMP=IFNULL(TEMP, values(TEMP)), 
        RELATIVE_HUMIDITY=IFNULL(RELATIVE_HUMIDITY, values(RELATIVE_HUMIDITY)), 
        WIND_SPEED=IFNULL(WIND_SPEED,values(WIND_SPEED)), 
        WIND_DIRECTION=IFNULL(WIND_DIRECTION,values(WIND_DIRECTION))
        """
        execute_many('sg_weather', sql, rows)
    if visibility:
        rows = [(*k, v['value']) for k, v in visibility.items()]
        sql = """
        insert into sg_visibility (STATION, PUB_TIME, VISIBILITY)
        values(%s, %s, %s)
        on duplicate key update VISIBILITY=values(VISIBILITY)
        """
        execute_many('sg_visibility', sql, rows)


def get_station(url_key, station, hours, key, weather, visibility):
    if station == 'Clear Results':
        return
    # station_code = stations.get(station)
    station_code = station
    if not station_code:
        raise ValueError('station {} not found'.format(station))
    # 'http://www.weather.gov.sg/wp-content/themes/wiptheme/page-functions/functions-ajax-rainfall-chart.php'
    # 'http://www.weather.gov.sg/wp-content/themes/wiptheme/page-functions/functions-ajax-temperature-chart.php'
    # 'http://www.weather.gov.sg/wp-content/themes/wiptheme/page-functions/functions-ajax-relative-humidity-chart.php'
    # 'http://www.weather.gov.sg/wp-content/themes/wiptheme/page-functions/functions-ajax-wind-chart.php'
    # 'http://www.weather.gov.sg/wp-content/themes/wiptheme/page-functions/functions-ajax-visibility-chart.php'
    if url_key in ['visibility', 'rainfall']:
        data_url = f'https://www.weather.gov.sg/wp-content/themes/wiptheme/page-functions/functions-weather-current-observations-{url_key}-data.php'
        params = {"station_code": station_code, "hrType": hours}
    else:
        data_url = f'https://www.weather.gov.sg/wp-content/themes/wiptheme/page-functions/functions-ajax-{url_key}-chart.php'
        params = {"stationCode": station_code, "hrType": hours}
    try:
        resp = requests.post(data_url, data=urlencode(params),
                             headers={'Content-Type': 'application/x-www-form-urlencoded'},
                             timeout=5)
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
        logger.error('request timeout, url: {}, params: {}'.format(data_url, params))
        return
    if not resp.ok:
        logger.error(f'request failed, url: {data_url}, params: {params}, status_code: {resp.status_code}')
        return
    station_e = PQ(resp.text)
    station_data = json.loads(station_e('p').html())
    if station_data:
        now = datetime.datetime.now()
        base_time = now.replace(minute=0, second=0, microsecond=0)
        # {'tableData': ['0.2', '0.2', '0.2', '0.2', '0.2', '4.6', '1.6', '0.8', '0.2', '0.2', '0.2', '0.2'], 'totalRainfall': 7.6}
        # {"temp": "26.6", "time": "16 Apr"}
        # {"rh": "78.5", "time": "16 Apr"}
        # {"windSpeedKpr": "2.4000", "time": "16 Apr", "windDirection": "24"}
        # {"value": 8, "time": "11 pm"}
        if key == 'rainfall':
            sample_data = station_data['tableData']
        else:
            # 将1minute的数据采样为1hour的数据
            sample_data = [d for idx, d in enumerate(station_data) if idx % 60 == 0]

        time_series = [base_time - datetime.timedelta(hours=i) for i in range(hours - 1, -1, -1)]
        for i in range(hours):
            item = sample_data[i]
            if isinstance(item, dict):
                item.pop('time')
            else:
                item = {'rainfall': item}  # rainfall
            if not item:
                continue
            if key == 'visibility':
                visibility[(station, time_series[i])].update(item)
            else:
                weather[(station, time_series[i])].update(item)
    # time.sleep(0.1)


if __name__ == '__main__':
    try:
        run(48)
    except RuntimeError:
        subject = 'sg-weather数据获取出错'
        content = traceback.format_exc()
        send_mail(
            mail_subject=subject,
            mail_content=content
        )
