from datetime import datetime
from django.conf import settings
import json
import math
from pprint import pprint
import urllib
from urllib.request import urlopen

ServiceKey = settings.WEATHER_API_KEY

# 날씨와 장소를 인자로 받아서 날씨 데이터 딕셔너리를 반환한다.
# 예시 input_date : 2020-03-31 15:26:23, location : "1" location index
def get_weather_date(input_date, location): 

    with open('apps/api/locations/data.json') as json_file:
        json_data = json.load(json_file)

    date = input_date.split()
    year_month_day = date[0].split('-')
    month = year_month_day[1]
    day = year_month_day[2]

    api_date = year_month_day[0] + year_month_day[1] + year_month_day[2]
    time = date[1].split(':')
    api_time =time[0] + time[1]

    convert_api_time, convert_api_date = convert_time(api_time, month, day)
    convert_api_date = year_month_day[0] + convert_api_date # year_month_day[0] -> 년도 년도 합쳐주기

    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?"
    key = "serviceKey=" + ServiceKey
    numOfRows = "&numOfRows=100"
    typeOfData = "&dataType=JSON"
    date = "&base_date=" + convert_api_date
    time = "&base_time=" + convert_api_time

    x = (json_data[str(location)]['x'])
    y = (json_data[str(location)]['y'])

    nx = "&nx=" + x
    ny = "&ny=" + y

    api_url = url + key + numOfRows + typeOfData + date + time + nx + ny
    data = urllib.request.urlopen(api_url).read().decode('utf8')
    data_json = json.loads(data)
    # get date and time
    parsed_json = data_json['response']['body']['items']['item']
    target_date = parsed_json[0]['fcstDate']
    target_time = parsed_json[0]['fcstTime']

    passing_data = {}
    for parsed in parsed_json:
        passing_data[parsed['category']] = parsed['fcstValue']

    t = passing_data['T3H']
    v = passing_data['WSD']
    t = float(t)
    v = float(v)
    
    # 체감 온도 계산
    wci = 13.12 + 0.6215 * t -  11.37 * math.pow(v, 0.16) + 0.3965 * t * math.pow(v, 0.16)
    wci = round(wci, 2)
    passing_data['WCI'] = wci

    t_high = passing_data['TMX']
    t_min = passing_data['TMN']
    t_high = float(t_high)
    t_min = float(t_min)

    wci_high = 13.12 + 0.6215*t_high - 11.37 * math.pow(v, 0.16) + 0.3965 * t_high * math.pow(v, 0.16)
    wci_high = round(wci_high, 2)
    wci_low = 13.12 + 0.6215*t_min - 11.37*math.pow(v, 0.16) + 0.3965 * t_min*math.pow(v, 0.16)
    wci_low = round(wci_low, 2)

    passing_data['WCI'] = wci # current wind chill temp
    passing_data['WCIMAX'] = wci_high # maximum chill temp
    passing_data['WCIMIN'] = wci_low # minium chill temp

    return passing_data

# 날씨 불러오기 날짜, 시간, location(index)
def get_weather_time_date(date, time, location):

    with open('apps/api/locations/data.json') as json_file:
        json_data = json.load(json_file)

    api_date = date
    api_time = time

    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?"
    key = "serviceKey=" + ServiceKey
    numOfRows = "&numOfRows=100"
    typeOfData = "&dataType=JSON"
    date = "&base_date=" + api_date
    time = "&base_time=" + api_time

    x = (json_data[str(location)]['x'])
    y = (json_data[str(location)]['y'])

    nx = "&nx=" + x
    ny = "&ny=" + y

    api_url = url + key + numOfRows + typeOfData + date + time + nx + ny
    data = urllib.request.urlopen(api_url).read().decode('utf8')
    data_json = json.loads(data)

    parsed_json = data_json['response']['body']['items']['item']
    target_date = parsed_json[0]['fcstDate']  # get date and time
    target_time = parsed_json[0]['fcstTime']
    date_calibrate = target_date #date of TMX, TMN
    passing_data = {}

    for parsed in parsed_json:
        passing_data[parsed['category']] = parsed['fcstValue']
    
    passing_data['T3H'] = float(passing_data['T3H'])
    
    t = passing_data['T3H'] # current 3hour temp
    v = passing_data['WSD'] # current wind speed

    t = float(t)
    v = float(v)
    
    t_high = passing_data['TMX']
    t_min = passing_data['TMN']

    t_high =float(t_high)
    t_min =float(t_high)

    wci = 13.12 + 0.6215*t - 11.37*math.pow(v, 0.16) + 0.3965*t*math.pow(v, 0.16)
    wci = round(wci, 2)

    wci_high = 13.12 + 0.6215*t_high - 11.37*math.pow(v, 0.16) + 0.3965*t_high*math.pow(v, 0.16)
    wci_high = round(wci, 2)
    wci_low = 13.12 + 0.6215*t_min - 11.37*math.pow(v, 0.16) + 0.3965*t_min*math.pow(v, 0.16)
    wci_low = round(wci, 2)

    passing_data['WCI'] = wci # current wind chill temp
    passing_data['WCIMAX'] = wci_high # maximum chill temp
    passing_data['WCIMIN'] = wci_low # minium chill temp

    return passing_data

# start_date와 end_date 사이에 날씨 API 발표시각이 있으면 중간 값 떼오기
def get_weather_between(start_input_date, end_input_date, location):

    with open('apps/api/locations/data_full_address.json') as json_file:
        json_data = json.load(json_file)

    start_date = start_input_date.split()
    start_year_month_day= start_date[0].split('-')
    start_month = start_year_month_day[1]
    start_day = start_year_month_day[2]

    # year_month_day = yyyymmzdd  yyyy -> 년 mm ->달 dd --> 일
    end_date = end_input_date.split()
    end_year_month_day = end_date[0].split('-')
    end_month = end_year_month_day[1]
    end_day = end_year_month_day[2]

    start_api_date = start_year_month_day[0] + start_year_month_day[1] + start_year_month_day[2]
    start_time = start_date[1].split(':')
    start_api_time =start_time[0] + start_time[1]
    convert_start_api_time, convert_start_api_date = convert_time(start_api_time, start_month, start_day)
    
    end_api_date = end_year_month_day[0] + end_year_month_day[1] + end_year_month_day[2]
    end_time = end_date[1].split(':')
    end_api_time =end_time[0] + end_time[1]
    convert_end_api_time, convert_end_api_date = convert_time(end_api_time, end_month, end_day)

    start_weather =  get_weather_date(start_input_date, location)
    end_weather = get_weather_date(end_input_date, location)

    start_T3H = int(start_weather['T3H'])
    end_T3H = int(end_weather['T3H'])

    weather_data = start_weather

    # api_time tiems1는 시간 xxyy xx -> 시간 yy -> 분
    # TODO(Jaeho) 사이 시간에 API 호출 시간이 있으면 호출 가능한 시간 온도도 다시 구해오기, 구현 완료 후 삭제
    # start와 end time 사이에 날씨 API 갱신 시간이 있으면 그시간을 불러옴
    if  int(convert_end_api_time) - int(convert_start_api_time) < 0: # 날짜가 바뀌면
        weather_data['MAX'] = max(start_T3H, end_T3H)
        weather_data['MIN'] = min(start_T3H, end_T3H)
        weather_data['WCIMAX'] = max(start_weather['WCIMAX'], end_weather['WCIMAX'])
        weather_data['WCIMIN'] = min(start_weather['WCIMIN'], end_weather['WCIMIN'])

    elif int(convert_end_api_time) - int(convert_start_api_time) < 300:
        weather_data['MAX'] = max(start_weather['T3H'], end_weather['T3H'])
        weather_data['MIN'] = min(start_weather['T3H'], end_weather['T3H'])
        weather_data['WCIMAX'] = max(start_weather['WCI'], end_weather['WCI'])
        weather_data['WCIMIN'] = min(start_weather['WCI'], end_weather['WCI'])

    elif int(convert_end_api_time) - int(convert_start_api_time) < 900:
        if(convert_start_api_time == "2300"):
            temp_time = "0200"
            temp_weather = get_weather_time_date(end_api_date, temp_time, location)
            weather_data['MIN'] = min(start_T3H, end_T3H, temp_weather['T3H'])
            weather_data['MAX'] = max(start_T3H, end_T3H, temp_weather['T3H'])
            weather_data['WCIMAX'] = max(start_weather['WCI'], end_weather['WCI'], temp_weather['WCI'])
            weather_data['WCIMIN'] = min(start_weather['WCI'], end_weather['WCI'], temp_weather['WCI'])

        else:
            temp_int = int(convert_start_api_time) # 날짜가 안바 뀔 때 3시간 뒤 날씨도 확인해서 더해주기
            temp_int += 300
            temp_time = str(temp_int)
            if temp_int // 1000 == 0:
                temp_time = "0" + temp_time
            temp_weather = get_weather_time_date(start_api_date, temp_time, location)
            weather_data['MIN'] = min(start_T3H, end_T3H, temp_weather['T3H'])
            weather_data['MAX'] = max(start_T3H, end_T3H, temp_weather['T3H'])
            weather_data['WCIMAX'] = max(start_weather['WCI'], end_weather['WCI'], temp_weather['WCI'])
            weather_data['WCIMIN'] = min(start_weather['WCI'], end_weather['WCI'], temp_weather['WCI'])

    elif int(convert_end_api_time) - int(convert_start_api_time) < 1500:
        if(convert_start_api_time == "1700" or "2000" ):
            temp_time = "0200"
            temp_weather = get_weather_time_date(end_api_date, temp_time, location)
            weather_data['MIN'] = min(start_T3H, end_T3H, temp_weather['T3H'])
            weather_data['MAX'] = max(start_T3H, end_T3H, temp_weather['T3H'])
            weather_data['WCIMAX'] = max(start_weather['WCI'], end_weather['WCI'], temp_weather['WCI'])
            weather_data['WCIMIN'] = min(start_weather['WCI'], end_weather['WCI'], temp_weather['WCI'])

        elif(convert_start_api_time == "2300"):
            temp_time = "0500"
            temp_weather = get_weather_time_date(end_api_date, temp_time, location)
            weather_data['MIN'] = min(start_T3H, end_T3H, temp_weather['T3H'])
            weather_data['MAX'] = max(start_T3H, end_T3H, temp_weather['T3H'])
            weather_data['WCIMAX'] = max(start_weather['WCI'], end_weather['WCI'], temp_weather['WCI'])
            weather_data['WCIMIN'] = min(start_weather['WCI'], end_weather['WCI'], temp_weather['WCI'])

        else:
            temp_int = int(convert_start_api_time) # 날짜가 안바 뀔 때 3시간 뒤 날씨도 확인해서 더해주기
            temp_int += 600
            temp_time = str(temp_int)
            if temp_int // 1000 == 0:
                temp_time = "0" + temp_time
            temp_weather = get_weather_time_date(start_api_date, temp_time, location)
            
            weather_data['MIN'] = min(start_T3H, end_T3H, temp_weather['T3H'])
            weather_data['MAX'] = max(start_T3H, end_T3H, temp_weather['T3H'])
            weather_data['WCIMAX'] = max(start_weather['WCI'], end_weather['WCI'], temp_weather['WCI'])
            weather_data['WCIMIN'] = min(start_weather['WCI'], end_weather['WCI'], temp_weather['WCI'])

    else:
        weather_data['MIN'] = min(start_weather['TMN'], end_weather['TMN'])
        weather_data['MAX'] = max(start_weather['TMX'], end_weather['TMX'])
        weather_data['WCIMAX'] = max(start_weather['WCIMAX'], end_weather['WCIMAX']) 
        weather_data['WCIMIN'] = min(start_weather['WCIMIN'], end_weather['WCIMIN'])
        
    return weather_data

# 입력 받은 시간을 API 요청가능 시간으로 바꿔주기
# 날씨 API에서 확정적으로 호출 가능한 시간은 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300 (1일 8회 3시간 간격)
def convert_time(time, month, day): 
    # 2시 이전일 때 전날 23:00 날씨를 받아옴

    day = int(day)
    month = int(month)
    
    if int(time) < 200: 
        day = day-1
        if day == 0 :
            if month == 5 or 7 or 10 or 12:
                day = 30
            elif month == 1 or 2 or 4 or 6 or 8 or 9 or 11:
                day = 31
            elif month == 3:
                day = 28

            month = month-1

        time = "2300"
    
    elif int(time) < 500: # 05:00 이전 일 때 02:00 날씨를 받아옴
        time = "0200"

    elif int(time) < 800: # 08:00 이전 일 때 05:00 날씨를 받아옴
        time = "0500"

    elif int(time) < 1100: # 11:00 이전 일 때 08:00 날씨를 받아옴
        time = "0800"
    
    elif int(time) < 1400: # 14:00 이전 일 때 14:00 날씨를 받아옴
        time = "1100"

    elif int(time) < 1700:  # 17:00 이전 일 때 14:00 날씨를 받아옴
        time = "1400"

    elif int(time) < 2000: # 20:00 이전 일 때 17:00 날씨를 받아옴
        time = "1700"

    elif int(time) < 2300:
        time = "2000"

    elif int(time) < 2400:
        time = "2300"

    
    if int(month) // 10 == 0:
        str_month = "0" + str(month)
    if int(day) // 10 == 0:
        str_day = "0" +str(day)
    date = str_month+str_day

    return time, date
