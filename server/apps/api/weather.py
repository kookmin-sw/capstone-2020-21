import json
import urllib
import datetime
import pytz
import math
from datetime import datetime
from urllib.request import urlopen
from pprint import pprint
from django.conf import settings







# ServiceKey = settings.WEATHER_API_KEY_1

def get_weather_date(input_date, location) : # 기본
    with open('apps/api/locations/data_full_address.json') as json_file:
        json_data = json.load(json_file)

    # ServiceKey = settings.SERVICE_API_KEY
    ServiceKey = settings.WEATHER_API_KEY_1


    days = input_date.split()
    times= days[0].split('-')

    api_date = times[0]+times[1]+times[2]
    times1 = days[1].split(':')
    api_time =times1[0]+times1[1]


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

    # print(api_url)

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
    wci_high = round(wci, 2)
    wci_low = 13.12 + 0.6215*t_min -  11.37*math.pow(v, 0.16) + 0.3965*t_min*math.pow(v, 0.16)
    wci_low = round(wci, 2)

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

    # ServiceKey = settings.SERVICE_API_KEY
        

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
    
    if  end_api_time - start_api_time > 3  : # 3시간 이상 6시간 미만 이면
        
        between_api_time = end_api_time - start_api_time

        between_data =  get_weather_by_time_date(start_api_date, first_api_time, location)

        between_T3H = float(between_data['T3H'])

        #MIN -> MAX TEMP
        passing_data['MINT'] = min(start_T3H, end_T3H, between_T3H)
        #MAX -> MIN TEMP
        passing_data['MAXT'] = max(start_T3H, end_T3H, between_T3H)

        passing_data['VVV'] = start_weather['WSD']
        
    #TODO
        

    return passing_data








# --------------------- test code -------------------------


# ServiceKey = "6ZRhW%2BwEgu8KSNzXCvAsAm8fyDQ3XnPWtfbiy6rtX7JAoPeXmQMq9%2FtSczPfnLd%2FnAnPdhnNkc60BAROfx2TEQ%3D%3D"
# with open('./locations/data_full_address.json') as json_file:
#     json_data = json.load(json_file)

# input_date = "2020-03-30 23:30"

# days = input_date.split()
# times= days[0].split('-')

# api_date = times[0]+times[1]+times[2]
# times1 = days[1].split(':')
# api_time =times1[0]+times1[1]
# print(api_date)
# print(api_time)

# url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?"
# key = "serviceKey=" + ServiceKey
# numOfRows = "&numOfRows=100"
# type = "&dataType=JSON"
# date = "&base_date=" + api_date
# time = "&base_time=" + api_time

# location = ""

# x = (json_data['경상남도 의령군 유곡면']['x'])
# y = (json_data['경상남도 의령군 유곡면']['y'])

# nx = "&nx=" + x
# ny = "&ny=" + y

# api_url = url + key + numOfRows + type + date + time + nx + ny
# print(date)
# print(api_url)
# data = urllib.request.urlopen(api_url).read().decode('utf8')
# data_json = json.loads(data)
# pprint(data_json)

# parsed_json = data_json['response']['body']['items']['item']

# target_date = parsed_json[0]['fcstDate']  # get date and time
# target_time = parsed_json[0]['fcstTime']

# date_calibrate = target_date #date of TMX, TMN
# # if target_time > '1300':
# #     date_calibrate = str(int(target_date) + 1)

# passing_data = {}
# for parsed in parsed_json:
#     passing_data[parsed['category']] = parsed['fcstValue']


# print(passing_data)

# print(passing_data['TMN'])
# t = passing_data['T3H']
# v = passing_data['WSD']
# t = float(t)
# v = float(v)
# print(t)
# print(v)
# # wci = (10*math.sqrt(v)-v+10.5)*(33-t)
# wci = 13.12 + 0.6215*t -  11.37*math.pow(v, 0.16) + 0.3965*t*math.pow(v, 0.16)
# wci = round(wci, 2)
# print(wci)