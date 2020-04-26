import config.settings.base

DJANGO_SETTINGS_MODULE = config.settings.base

import schedule
import time
import datetime
from decouple import config
from apps.api.weather import *
from apps.api.models import Weather

def run():
    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    print(now)

    for i in range(3780):
        response = get_weather_date(now, str(i))

        # WCI 체감온도 T3H 기온 WSD 풍속 REH 습도 R06 강수량
        Weather.objects.create(location_code=i, date=now[0:10], time=now[11:13], 
                                temp=response['T3H'], sensible_temp=response['WCI'], humidity=response['REH'], 
                                wind_speed=response['WSD'], precipitation=response['R06'])
                            
# basetime 11분 뒤 마다 basetime에 대한 날씨정보를 저장해야 함
schedule.every().day.at("02:11").do(run)
schedule.every().day.at("05:11").do(run)
schedule.every().day.at("08:11").do(run)
schedule.every().day.at("11:11").do(run)
schedule.every().day.at("14:11").do(run)
schedule.every().day.at("17:11").do(run)
schedule.every().day.at("20:11").do(run)
schedule.every().day.at("23:11").do(run)

while True:
    schedule.run_pending()
