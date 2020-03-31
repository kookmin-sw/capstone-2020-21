import json
import urllib
import datetime
import pytz
import math
from datetime import datetime
from django.conf import settings
from urllib.request import urlopen
from pprint import pprint

ServiceKey = settings.WEATHER_API_KEY_1
# ServiceKey = settings.SERVICE_API_KEY

def get_weather_date(input_date, location) : # 기본

    with open('apps/api/locations/data_full_address.json') as json_file:
        json_data = json.load(json_file)

    days = input_date.split()
    times= days[0].split('-')

    month = times[1]
    day = times[2]

    api_date = times[0]+times[1]+times[2]
    times1 = days[1].split(':')
    api_time =times1[0]+times1[1]

    # print(month)
    # print(day)

    convert_api_time, convert_api_date = convert_time(api_time, month, day)

    convert_api_date = times[0] + convert_api_date # times[0] -> 년도 년도 합쳐주기
    # print( "convert_time : " + convert_api_time)
    # print("convert_date : " + convert_api_date)

    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?"
    key = "serviceKey=" + ServiceKey
    numOfRows = "&numOfRows=100"
    type = "&dataType=JSON"
    date = "&base_date=" + convert_api_date
    time = "&base_time=" + convert_api_time

    x = (json_data[location]['x'])
    y = (json_data[location]['y'])

    nx = "&nx=" + x
    ny = "&ny=" + y

    api_url = url + key + numOfRows + type + date + time + nx + ny

    # print(api_url)

    data = urllib.request.urlopen(api_url).read().decode('utf8')
    data_json = json.loads(data)
    # pprint(data_json)

    parsed_json = data_json['response']['body']['items']['item']
    target_date = parsed_json[0]['fcstDate']  # get date and time
    target_time = parsed_json[0]['fcstTime']

    # date_calibrate = target_date #date of TMX, TMN
    # if target_time > '1300':
    #     date_calibrate = str(int(target_date) + 1)

    passing_data = {}
    for parsed in parsed_json:
        passing_data[parsed['category']] = parsed['fcstValue']


    # parsed_json = data_json['response']['body']['items']['item']

    # target_date = parsed_json[0]['fcstDate']  # get date and time
    # target_time = parsed_json[0]['fcstTime']

    # date_calibrate = target_date #date of TMX, TMN
    # # if target_time > '1300':
    # #     date_calibrate = str(int(target_date) + 1)

    passing_data = {}
    for parsed in parsed_json:
        passing_data[parsed['category']] = parsed['fcstValue']
    
    
    t = passing_data['T3H']
    v = passing_data['WSD']
    t = float(t)
    v = float(v)
    
    wci = 13.12 + 0.6215*t -  11.37*math.pow(v, 0.16) + 0.3965*t*math.pow(v, 0.16)
    wci = round(wci, 2)
    passing_data['WCI'] = wci

    t_high = passing_data['TMX']
    t_min = passing_data['TMN']
    t_high = float(t_high)
    t_min = float(t_min)

    
   
    wci_high = 13.12 + 0.6215*t_high -  11.37*math.pow(v, 0.16) + 0.3965*t_high*math.pow(v, 0.16)
    wci_high = round(wci_high, 2)
    wci_low = 13.12 + 0.6215*t_min -  11.37*math.pow(v, 0.16) + 0.3965*t_min*math.pow(v, 0.16)
    wci_low = round(wci_low, 2)

    passing_data['WCI'] = wci # current wind chill temp
    passing_data['WCIMAX'] = wci_high #maximum chill temp
    passing_data['WCIMIN'] = wci_low #minium chill temp

    return passing_data

def get_weather_by_time_date(date, time, location) :

    with open('apps/api/locations/data_full_address.json') as json_file:
        json_data = json.load(json_file)

    api_date = date
    api_time = time

    # print(api_date)
    # print(api_time)

    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?"
    key = "serviceKey=" + ServiceKey
    numOfRows = "&numOfRows=100"
    type = "&dataType=JSON"
    date = "&base_date=" + api_date
    time = "&base_time=" + api_time

    x = (json_data[location]['x'])
    y = (json_data[location]['y'])

    nx = "&nx=" + x
    ny = "&ny=" + y

    api_url = url + key + numOfRows + type + date + time + nx + ny
    data = urllib.request.urlopen(api_url).read().decode('utf8')
    data_json = json.loads(data)
    pprint(data_json)

    parsed_json = data_json['response']['body']['items']['item']

    target_date = parsed_json[0]['fcstDate']  # get date and time
    target_time = parsed_json[0]['fcstTime']

    date_calibrate = target_date #date of TMX, TMN
    # if target_time > '1300':
    #     date_calibrate = str(int(target_date) + 1)

    passing_data = {}
    for parsed in parsed_json:
        passing_data[parsed['category']] = parsed['fcstValue']
    
    t = passing_data['T3H'] # current 3hour temp
    v = passing_data['WSD'] # current 

    t = float(t)
    v = float(v)
    
    t_high = passing_data['TMX']
    t_min = passing_data['TMN']

    wci = 13.12 + 0.6215*t -  11.37*math.pow(v, 0.16) + 0.3965*t*math.pow(v, 0.16)
    wci = round(wci, 2)

    wci_high = 13.12 + 0.6215*t_high -  11.37*math.pow(v, 0.16) + 0.3965*t_high*math.pow(v, 0.16)
    wci_high = round(wci, 2)
    wci_low = 13.12 + 0.6215*t_min -  11.37*math.pow(v, 0.16) + 0.3965*t_min*math.pow(v, 0.16)
    wci_low = round(wci, 2)

    passing_data['WCI'] = wci # current wind chill temp
    passing_data['WCIMAX'] = wci_high #maximum chill temp
    passing_data['WCIMIN'] = wci_low #minium chill temp

    return passing_data

def get_weather_between(start_date, end_date, location) :

    with open('apps/api/locations/data_full_address.json') as json_file:
        json_data = json.load(json_file)
        
    start_days = start_date.split()
    start_times= start_days[0].split('-')
    #times = yyyymmzdd  yyyy -> 년 mm ->달 dd --> 일
    end_days = end_date.split()
    end_times = end_date.spilt()

    start_api_date = start_times[0]+start_times[1]+start_times[2]
    start_times1 = start_days[1].split(':')
    start_api_time =start_times1[0]+start_times1[1]

    end_api_date = end_times[0]+end_times[1]+end_times[2]
    end_times1 = end_days[1].split(':')
    end_api_time =end_times1[0]+end_times1[1]
    
    start_weather =  get_weather_date(start_date, location)
    end_weather = get_weather_date(end_date, location)

    start_T3H = float(start_weather['T3H'])
    end_T3H = float(end_weather['T3H'])

    passing_data = {}
    #api_time tiems1는 시간 xxyy xx -> 시간 yy -> 분
    #TODO 사이 시간에 API 호출 시간이 있으면 그시간 온도도 다시 구해오기
    if  end_api_time - start_api_time > 3  : # 3시간 이상 6시간 미만 이면
        between_api_time = end_api_time - start_api_time
        between_data =  get_weather_by_time_date(start_api_date, first_api_time, location)
        between_T3H = float(between_data['T3H'])
        #MIN -> MAX TEMP
        passing_data['MINT'] = min(start_T3H, end_T3H, between_T3H)
        #MAX -> MIN TEMP
        passing_data['MAXT'] = max(start_T3H, end_T3H, between_T3H)
        passing_data['VVV'] = start_weather['WSD']
        
    return passing_data

def convert_time(time, month, day) : #입력 받은 시간을 API 요청가능 시간으로 바꿔주기

    if int(time) < 200 :
        print("passed in < 200")
        day =int(day)
        day = day-1
        month = int(month)
        if day == 0 :
            if month == 5 or 7 or 10 or 12 :
                day = 30

            elif month == 1 or 2 or 4 or 6 or 8 or 9 or 11 :
                day = 31

            elif month == 3 :
                day = 28
            
            month = month-1

            str_month = str(month)

            if(month/10 == 0) :
                str_month = "0" + str_month

            if int(day) / 10 == 0 :
                str_day = "0" +str(day)

        time = "2300"
    
    elif int(time) < 500 :

        time = "0200"

    elif int(time) < 800 :
        print('passed in <800')
        time = "0500"

    elif int(time) < 1100 :

        time = "0800"
    
    elif int(time) < 1400 :

        time = "1100"

    elif int(time) < 1700 :

        time = "1400"

    elif int(time) < 2000 :

        time = "1700"

    elif int(time) < 2300 :

        time = " 2000"

    elif int(time) < 2400 :

        time = "2300"

    str_day = str(day) 
    str_month = str(month)
    # print(str_day)
    # print(str_month)

    date = str_month+str_day
    # print("time : " +  time)

    return time, date
