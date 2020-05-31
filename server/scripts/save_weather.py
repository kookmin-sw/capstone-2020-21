import config.settings.base

DJANGO_SETTINGS_MODULE = config.settings.base

import schedule
import time
import datetime
import threading
from decouple import config
from apps.api.weather import *
from apps.api.models import Weather

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def run():
    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    # TODO(hyobin) : print문 지우기
    print(now)

    date = now.split()
    year_month_day = date[0].split('-')
    year = year_month_day[0]
    month = year_month_day[1]
    day = year_month_day[2]

    conv_time = date[1].split(':')
    conv_time = conv_time[0] + conv_time[1]
    conv_time, conv_date = convert_time(conv_time, year, month, day)

    with open('apps/api/locations/data.json') as json_file:
        json_data = json.load(json_file)

    err_location_code = []

    for location in range(3780):
        new_x = int((json_data[str(location)]['x']))
        new_y = int((json_data[str(location)]['y']))

        weather_filtering = Weather.objects.filter(date=now[0:10], time=conv_time[0:2], x=new_x, y=new_y)
        if weather_filtering.exists():
            # TODO(hyobin) : print문 지우기
            print("old x: ", new_x, " y : ", new_y)
            Weather.objects.create(location_code=location, date=now[0:10], time=conv_time[0:2], x=new_x, y=new_y,
                                temp=weather_filtering[0].temp, sensible_temp=weather_filtering[0].sensible_temp,
                                humidity=weather_filtering[0].humidity, wind_speed=weather_filtering[0].wind_speed,
                                precipitation=weather_filtering[0].precipitation)

            continue

        # TODO(hyobin) : print문 지우기
        print("new x: ", new_x, " y : ", new_y)

        try:
            response = get_weather_date(now, str(location))

            # WCI 체감온도 T3H 기온 WSD 풍속 REH 습도 R06 강수량
            Weather.objects.create(location_code=location, date=now[0:10], time=conv_time[0:2], x=new_x, y=new_y,
                                    temp=response['T3H'], sensible_temp=response['WCI'], humidity=response['REH'],
                                    wind_speed=response['WSD'], precipitation=response['R06'])
            
        except Exception:
            err_location_code.append(location)

    while len(err_location_code) != 0:
        time.sleep(600)
        for location in range(len(err_location_code)):
            try:
                response = get_weather_date(now, str(err_location_code[location]))

                # WCI 체감온도 T3H 기온 WSD 풍속 REH 습도 R06 강수량
                Weather.objects.create(location_code=err_location_code[location], date=now[0:10], time=conv_time[0:2], x=new_x, y=new_y,
                                        temp=response['T3H'], sensible_temp=response['WCI'], humidity=response['REH'],
                                        wind_speed=response['WSD'], precipitation=response['R06'])
                del err_location_code[location]

            except Exception:
                continue


def run_time(tString):
    now = tString
    date = now.split()
    year_month_day = date[0].split('-')
    year = year_month_day[0]
    month = year_month_day[1]
    day = year_month_day[2]

    conv_time = date[1].split(':')
    conv_time = conv_time[0] + conv_time[1]
    conv_time, conv_date = convert_time(conv_time, year, month, day)

    with open('apps/api/locations/data.json') as json_file:
        json_data = json.load(json_file)

    err_location_code = []

    for location in range(3780):
        new_x = int((json_data[str(location)]['x']))
        new_y = int((json_data[str(location)]['y']))

        weather_filtering = Weather.objects.filter(date=now[0:10], time=conv_time[0:2], x=new_x, y=new_y)
        if weather_filtering.exists():
            # TODO(hyobin) : print문 지우기
            print("old x: ", new_x, " y : ", new_y)
            Weather.objects.create(location_code=location, date=now[0:10], time=conv_time[0:2], x=new_x, y=new_y,
                                temp=weather_filtering[0].temp, sensible_temp=weather_filtering[0].sensible_temp,
                                humidity=weather_filtering[0].humidity, wind_speed=weather_filtering[0].wind_speed,
                                precipitation=weather_filtering[0].precipitation)

            continue

        # TODO(hyobin) : print문 지우기
        print("new x: ", new_x, " y : ", new_y)

        try:
            response = get_weather_date(now, str(location))

            # WCI 체감온도 T3H 기온 WSD 풍속 REH 습도 R06 강수량
            Weather.objects.create(location_code=location, date=now[0:10], time=conv_time[0:2], x=new_x, y=new_y,
                                    temp=response['T3H'], sensible_temp=response['WCI'], humidity=response['REH'],
                                    wind_speed=response['WSD'], precipitation=response['R06'])
            
        except Exception:
            err_location_code.append(location)

    while len(err_location_code) != 0:
        time.sleep(600)
        for location in range(len(err_location_code)):
            try:
                response = get_weather_date(now, str(err_location_code[location]))

                # WCI 체감온도 T3H 기온 WSD 풍속 REH 습도 R06 강수량
                Weather.objects.create(location_code=err_location_code[location], date=now[0:10], time=conv_time[0:2], x=new_x, y=new_y,
                                        temp=response['T3H'], sensible_temp=response['WCI'], humidity=response['REH'],
                                        wind_speed=response['WSD'], precipitation=response['R06'])
                del err_location_code[location]

            except Exception:
                continue

def ago():
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=7)
    data = Weather.objects.filter(date__lte=last_week)
    data.delete()

job1 = threading.Thread(target=run_time, args=['2020-05-28 20:30:00'])
job2 = threading.Thread(target=run_time, args=['2020-05-28 23:30:00'])

job1.start()
job2.start()


# basetime 30분 뒤 마다 basetime에 대한 날씨정보를 저장
schedule.every().day.at("02:30").do(run_threaded, run)
schedule.every().day.at("05:30").do(run_threaded, run)
schedule.every().day.at("08:30").do(run_threaded, run)
schedule.every().day.at("11:30").do(run_threaded, run)
schedule.every().day.at("14:30").do(run_threaded, run)
schedule.every().day.at("17:30").do(run_threaded, run)
schedule.every().day.at("20:30").do(run_threaded, run)
schedule.every().day.at("23:30").do(run_threaded, run)

# 현재 기준 7일 전의 날씨정보 삭제
schedule.every().day.at("00:00").do(run_threaded, ago)

while True:
    schedule.run_pending()

    