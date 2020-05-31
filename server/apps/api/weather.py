import datetime
from django.conf import settings
import json
import math
import urllib
import pprint
from urllib.request import urlopen

ServiceKey = settings.WEATHER_API_KEY


def get_weather_date(input_date, location): 
    """
     날씨와 장소를 인자로 받아서 날씨 데이터 딕셔너리를 반환한다.
     예시 input_date : 2020-03-31 15:26:23, location : "1" location index
    """
    with open('apps/api/locations/data.json') as json_file:
        json_data = json.load(json_file)

    date = input_date.split()
    year_month_day = date[0].split('-')
    year = year_month_day[0]
    month = year_month_day[1]
    day = year_month_day[2]

    time = date[1].split(':')
    api_time =time[0] + time[1]

    convert_api_time, convert_api_date = convert_time(api_time, year, month, day)
    convert_api_date = convert_api_date # year_month_day[0] -> 년도 년도 합쳐주기
    # TODO : print 지우고 commit
    print(convert_api_date)

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
    # TODO : print 지우고 commit
    print(data)
    data_json = json.loads(data)
    # get date and time
    parsed_json = data_json['response']['body']['items']['item']

    passing_data = {}
    for parsed in parsed_json:
        passing_data[parsed['category']] = parsed['fcstValue']

    t = passing_data['T3H']
    v = passing_data['WSD']
    t = float(t)
    v = float(v)
    
    # 체감 온도 계산
    wci = getWCI(t, v)
    wci = round(wci, 2)

    t_high = passing_data['TMX']
    t_min = passing_data['TMN']
    t_high = float(t_high)
    t_min = float(t_min)

    wci_high = getWCI(t_high, v)
    wci_high = round(wci, 2)
    wci_low = getWCI(t_min, v)
    wci_low = round(wci, 2)


    passing_data['WCI'] = wci # current wind chill temp
    passing_data['WCIMAX'] = wci_high # maximum chill temp
    passing_data['WCIMIN'] = wci_low # minium chill temp

    return passing_data

# 날씨 불러오기 날짜, 시간, location(index)
def get_weather_time_date(date, time, location):
    # convert_time으로 변환된 시간과 장소를 입력 받아 get_weather_between에 필요한 기상 데이터를 딕셔너니로 반환한다.
    # 예시 : 2020-04-07 08:45, 2020-04-07 22:24, location : "1" location index

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

    wci = getWCI(t, v)
    wci = round(wci, 2)

    wci_high = getWCI(t_high, v)
    wci_high = round(wci, 2)
    wci_low = getWCI(t_min, v)
    wci_low = round(wci, 2)

    passing_data['WCI'] = wci # current wind chill temp
    passing_data['WCIMAX'] = wci_high # maximum chill temp
    passing_data['WCIMIN'] = wci_low # minium chill temp

    return passing_data

def get_weather_between(start_input_date, end_input_date, location):
    """
     입력 받은 두 기간 내의 최저 최고 온도를 받으며 날씨 데이터를 weather_data로 반환한다.
     예시 : 2020-04-07 08:45, 2020-04-07 22:24, location : "1" location index
    """
    with open('apps/api/locations/data_full_address.json') as json_file:
        json_data = json.load(json_file)

    start_date = start_input_date.split()
    start_year_month_day= start_date[0].split('-')
    start_year = start_year_month_day[0]
    start_month = start_year_month_day[1]
    start_day = start_year_month_day[2]

    # year_month_day = yyyymmzdd  yyyy -> 년 mm ->달 dd --> 일

    end_date = end_input_date.split()
    end_year_month_day = end_date[0].split('-')
    end_year = end_year_month_day[0]
    end_month = end_year_month_day[1]
    end_day = end_year_month_day[2]

    start_api_date = start_year_month_day[0] + start_year_month_day[1] + start_year_month_day[2]
    start_time = start_date[1].split(':')
    start_api_time =start_time[0] + start_time[1]
    convert_start_api_time, convert_start_api_date = convert_time(start_api_time, start_year, start_month, start_day)
    
    end_api_date = end_year_month_day[0] + end_year_month_day[1] + end_year_month_day[2]
    end_time = end_date[1].split(':')
    end_api_time =end_time[0] + end_time[1]
    convert_end_api_time, convert_end_api_date = convert_time(end_api_time, end_year, end_month, end_day)

    start_weather =  get_weather_date(start_input_date, location)
    end_weather = get_weather_date(end_input_date, location)

    start_T3H = float(start_weather['T3H'])
    end_T3H = float(end_weather['T3H'])

    weather_data = start_weather

    # api_time tiems1는 시간 xxyy xx -> 시간 yy -> 분
    # 중간 시점 temp_time을 구해 중간 시간, 시작 시간, 종료 시간 세 구간의 온도를 고려해 기준 내 최저 최고 온도를 구한다.

    if int(convert_end_api_time) - int(convert_start_api_time) < 0: # 날짜가 바뀌면
        weather_data['MAX'] = max(float(start_T3H), float(end_T3H))
        weather_data['MIN'] = min(float(start_T3H), float(end_T3H))
        weather_data['WCIMAX'] = max(float(start_weather['WCIMAX']), float(end_weather['WCIMAX']))
        weather_data['WCIMIN'] = min(float(start_weather['WCIMIN']), float(end_weather['WCIMIN']))

    elif int(convert_end_api_time) - int(convert_start_api_time) < 300:
        weather_data['MAX'] = max(float(start_weather['T3H']), float(end_weather['T3H']))
        weather_data['MIN'] = min(float(start_weather['T3H']), float(end_weather['T3H']))
        weather_data['WCIMAX'] = max(float(start_weather['WCI']), float(end_weather['WCI']))
        weather_data['WCIMIN'] = min(float(start_weather['WCI']), float(end_weather['WCI']))

    elif int(convert_end_api_time) - int(convert_start_api_time) < 900:
        if(convert_start_api_time == "2300"):
            temp_time = "0200"
            temp_weather = get_weather_time_date(end_api_date, temp_time, location)
            weather_data['MIN'] = min(start_T3H, end_T3H, float(temp_weather['T3H']))
            weather_data['MAX'] = max(start_T3H, end_T3H, float(temp_weather['T3H']))
            weather_data['WCIMAX'] = max(float(start_weather['WCI']), float(end_weather['WCI']), float(temp_weather['WCI']))
            weather_data['WCIMIN'] = min(float(start_weather['WCI']), float(end_weather['WCI']), float(temp_weather['WCI']))

        else:
            temp_int = int(convert_start_api_time) # 날짜가 안바 뀔 때 3시간 뒤 날씨도 확인
            temp_int += 300
            temp_time = str(temp_int)
            if temp_int // 1000 == 0:
                temp_time = "0" + temp_time
            temp_weather = get_weather_time_date(start_api_date, temp_time, location)
            weather_data['MIN'] = min(start_T3H, end_T3H, float(temp_weather['T3H']))
            weather_data['MAX'] = max(start_T3H, end_T3H, float(temp_weather['T3H']))
            weather_data['WCIMAX'] = max(float(start_weather['WCI']), float(end_weather['WCI']), float(temp_weather['WCI']))
            weather_data['WCIMIN'] = min(float(start_weather['WCI']), float(end_weather['WCI']), float(temp_weather['WCI']))

    elif int(convert_end_api_time) - int(convert_start_api_time) < 1500:

        if convert_start_api_time == "1700" or convert_start_api_time == "2000":
            temp_time = "0200"
            temp_weather = get_weather_time_date(end_api_date, temp_time, location)
            weather_data['MIN'] = min(start_T3H, end_T3H, float(temp_weather['T3H']))
            weather_data['MAX'] = max(start_T3H, end_T3H, float(temp_weather['T3H']))
            weather_data['WCIMAX'] = max(float(start_weather['WCI']), float(end_weather['WCI']), float(temp_weather['WCI']))
            weather_data['WCIMIN'] = min(float(start_weather['WCI']), float(end_weather['WCI']), float(temp_weather['WCI']))

        elif convert_start_api_time == "2300":
            temp_time = "0500"
            temp_weather = get_weather_time_date(end_api_date, temp_time, location)
            weather_data['MIN'] = min(start_T3H, end_T3H, float(temp_weather['T3H']))
            weather_data['MAX'] = max(start_T3H, end_T3H, float(temp_weather['T3H']))
            weather_data['WCIMAX'] = max(float(start_weather['WCI']), float(end_weather['WCI']), float(temp_weather['WCI']))
            weather_data['WCIMIN'] = min(float(start_weather['WCI']), float(end_weather['WCI']), float(temp_weather['WCI']))

        else:
            temp_int = int(convert_start_api_time) # 날짜가 안바 뀔 때 6시간 뒤 날씨도 확인
            temp_int += 600
            temp_time = str(temp_int)
            if temp_int // 1000 == 0:
                temp_time = "0" + temp_time
            temp_weather = get_weather_time_date(start_api_date, temp_time, location)
            
            weather_data['MIN'] = min(start_T3H, end_T3H, float(temp_weather['T3H']))
            weather_data['MAX'] = max(start_T3H, end_T3H, float(temp_weather['T3H']))
            weather_data['WCIMAX'] = max(float(start_weather['WCI']), float(end_weather['WCI']), float(temp_weather['WCI']))
            weather_data['WCIMIN'] = min(float(start_weather['WCI']), float(end_weather['WCI']), float(temp_weather['WCI']))

    else: 
        weather_data['MIN'] = min(float(start_weather['TMN']), float(end_weather['TMN']))
        weather_data['MAX'] = max(float(start_weather['TMX']), float(end_weather['TMX']))
        weather_data['WCIMAX'] = max(float(start_weather['WCIMAX']), float(end_weather['WCIMAX']))
        weather_data['WCIMIN'] = min(float(start_weather['WCIMIN']), float(end_weather['WCIMIN']))
        
    return weather_data

def get_current_weather(location): 
    """
    장소를 인자로 받아서 날씨 데이터 딕셔너리를 반환한다.
    location : "1" location index
    제공되는 날씨 데이터에서 최저 최고 기온은 기상예보에서 받아온 이후 3~4시간 내에서의 최저 최고 기온이다.
    """
    with open('apps/api/locations/data.json') as json_file:
        json_data = json.load(json_file)

    now = datetime.datetime.now()

    # 현재 시간
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    hour = str(now.hour)
    minute = str(now.minute)

    if int(month) // 10 == 0:
        month = "0" + str(month)
    
    if int(day) // 10 == 0:
        day = "0" + str(day)

    if int(hour) // 10 == 0:
        hour = "0" + str(hour)

    if int(minute) // 10 == 0:
        minute = "0" + str(minute)

    api_time = hour + minute

    convert_api_time, convert_api_date = convert_fcst_time(api_time, year, month, day)
    convert_api_date = convert_api_date # year_month_day[0] -> 년도 년도 합쳐주기

    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtFcst?"
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
    parsed_json = data_json['response']['body']['items']['item']
    data_size = int(len(parsed_json)/10) # 받아온 시간의 수
    passing_data = {}

    min = 99.9
    max = -99.9
    passing_data_set = [] # 시간대 별로 저장할 리스트
    for i in range(0,data_size):
        passing_data_set.append({})
        for j in range(0,10):
            weather = parsed_json[(j*data_size)+i]
            passing_data_set[i][weather['category']] = weather['fcstValue']
    max = -999
    min = 999
    max_WSD = 0
    min_WSD = 100

    for i in range(0,data_size):
        if float(passing_data_set[i]['T1H']) > float(max):
            max = passing_data_set[i]['T1H']
            max_WSD = passing_data_set[i]['WSD']

        if float(passing_data_set[i]['T1H']) < float(min):
            min = passing_data_set[i]['T1H']
            min_WSD = passing_data_set[i]['WSD']
        
    passing_data = passing_data_set[0]
    t = passing_data['T1H']
    v = passing_data['WSD']
    t = float(t)
    v = float(v)

    # 체감 온도 계산
    wci = getWCI(t, v)
    wci = round(wci, 2)

    # api 초단기예보 중 최저 최고온도 구하기
    wci_max = getWCI(float(max), float(max_WSD))
    wci_max = round(wci_max, 2)
    wci_min = getWCI(float(min), float(min_WSD))
    wci_min = round(wci_min, 2)

    passing_data['MAX'] = max
    passing_data['MIN'] = min
    passing_data['WCI'] = wci # current wind chill temp
    passing_data['WCIMIN'] = wci_min
    passing_data['WCIMAX'] = wci_max

    return passing_data

def convert_time(time, year, month, day):
    """ 
     입력 받은 시간을 API 요청가능 시간으로 변환한다.
     예시 : 1230, 2020, 04, 07 (시간, 년도, 달, 날짜)
     날씨 API에서 확정적으로 호출 가능한 시간(Basetime)은 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300 (1일 8회 3시간 간격)
     날씨 API에서 Basetime 제공 시간은 Basetime 에서 10분 뒤이다.
     2시 이전일 때 전날 23:00 날씨를 받아온다.
    """

    year = int(year)
    day = int(day)
    month = int(month)
    str_day = str(day)
    str_month = str(month)
    current_date = datetime.date(year, month, day)
    subtracted_date = current_date - datetime.timedelta(days=1)
    if int(time) < 211: # 2시 11분 이전 일 때
        year = subtracted_date.year
        month = subtracted_date.month
        day = subtracted_date.day

        time = "2300"

    elif int(time) < 511: # 05:11 이전 일 때 02:00 날씨를 받아옴
        time = "0200"

    elif int(time) < 811: # 08:11 이전 일 때 05:00 날씨를 받아옴
        time = "0500"

    elif int(time) < 1111: # 11:11 이전 일 때 08:00 날씨를 받아옴
        time = "0800"
    
    elif int(time) < 1411: # 14:11 이전 일 때 14:00 날씨를 받아옴
        time = "1100"

    elif int(time) < 1711:  # 17:11 이전 일 때 14:00 날씨를 받아옴
        time = "1400"

    elif int(time) < 2011: # 20:11 이전 일 때 17:00 날씨를 받아옴
        time = "1700"

    elif int(time) < 2311: # 23: 11 이전 일 때 20:00 날씨를 받아옴
        time = "2000"

    elif int(time) < 2400: # 24: 00 이전 일 때 20:00 날씨를 받아옴. 
        time = "2300"
    
    if int(month) // 10 == 0:
        str_month = "0" + str(month)
    else:
        str_month = str(month)
    if int(day) // 10 == 0:
        str_day = "0" + str(day)
    else:
        str_day = str(day)

    date = str(year) + str_month + str_day

    return time, date

def convert_fcst_time(time, year, month, day):
    """ 
     입력 받은 시간을 API 요청가능 시간으로 변환한다.
     예시 : 1230, 2020, 04, 07 (시간, 년도, 달, 날짜)
     날씨 API에서 확정적으로 호출 가능한 시간(Basetime)은 0030 부터 1시간 간격 basetime 호출 가능 시간은 45분부터이다.
    """

    year = int(year)
    day = int(day)
    month = int(month)
    str_day = str(day)
    str_month = str(month)
    current_date = datetime.date(year, month, day)
    subtracted_date = current_date - datetime.timedelta(days=1)
    if int(time) < 1: # 0시 46분 이전 일 때
        year = subtracted_date.year
        month = subtracted_date.month
        day = subtracted_date.day

        time = "2330"

    elif int(time) < 146:
        time = "0030"

    elif int(time) < 246: 
        time = "0130"

    elif int(time) < 346:
        time = "0230"
    
    elif int(time) < 446:
        time = "0330"

    elif int(time) < 546:
        time = "0430"

    elif int(time) < 646:
        time = "0530"

    elif int(time) < 746: 
        time = "0630"

    elif int(time) < 846:
        time = "0730"
    
    elif int(time) < 946:
        time = "0830"

    elif int(time) < 1046:
        time = "0930"

    elif int(time) < 1146:
        time = "1030"
    
    elif int(time) < 1246:
        time = "1130"

    elif int(time) < 1346:
        time = "1230"

    elif int(time) < 1446:
        time = "1330"

    elif int(time) < 1546: 
        time = "1430"

    elif int(time) < 1646:
        time = "1530"
    
    elif int(time) < 1746:
        time = "1630"

    elif int(time) < 1846:
        time = "1730"

    elif int(time) < 1946:
        time = "1830"

    elif int(time) < 2046:
        time = "1930"

    elif int(time) < 2146: 
        time = "2030"

    elif int(time) < 2246:
        time = "2130"
    
    elif int(time) < 2346:
        time = "2230"

    elif int(time) < 2401:
        time = "2330"
    
    if int(month) // 10 == 0:
        str_month = "0" + str(month)
    if int(day) // 10 == 0:
        str_day = "0" + str(day)

    date = str(year) + str_month + str_day

    return time, date

# 체감 온도 구하기
def getWCI(temperature, wind_velocity): 
    """
     기온과 풍속을 입력 받아 체감온도를 반환한다.
     예시 : 12, 9.5
    """
    WCI = 13.12 + 0.6215 * temperature - 11.37 * math.pow(wind_velocity, 0.16) + 0.3965 * temperature * math.pow(wind_velocity, 0.16)
 
    return WCI
