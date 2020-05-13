import datetime
from django.conf import settings
import json
import math
import urllib
import pprint
from urllib.request import urlopen

ServiceKey = settings.GLOBAL_WEATHER_API_KEY

def find_city_id(city_name):
    with open('apps/api/locations/cities_20000.json', 'rt', encoding='UTF8') as json_file:
        json_data = json.load(json_file)
    city_id = 0
    for i in json_data:
        if i['city_name'] == city_name:
            city_id = i['city_id']
            break
    
    return city_id

def get_global_weather_city_id(forecast_date, city_id): 
    """
     16일 이내 날짜와 도시 ID를 입력받아 날씨정보를 반환한다.
     예시 input_date : 2020-03-31, city_id : "735563"
    """
    passing_data = {}
    url = "https://api.weatherbit.io/v2.0/forecast/daily?"
    city_id_url = "city_id=" + city_id
    key = "&key=" + ServiceKey

    api_url = url + city_id_url + key
    data = urllib.request.urlopen(api_url).read().decode('utf8')
    data_json = json.loads(data)
    parsed_json = data_json['data']

    for i in parsed_json:
        if i['datetime'] == forecast_date:
            passing_data['WSD'] = i['wind_spd']
            passing_data['TEMP'] = i['temp']
            passing_data['TMX'] = i['max_temp']
            passing_data['TMN'] = i['min_temp']
            passing_data['REH'] = i['rh']
            passing_data['POP'] = i['pop']
            passing_data['PRE'] = i['precip']

    t = passing_data['TEMP']
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

def get_global_weather_city_name(forecast_date, city_name): 
    """
     16일 이내 날짜와 도시를 입력받아 날씨정보를 반환한다.
     예시 input_date : 2020-03-31, city_name : "Seoul"
    """
    passing_data = {}
    url = "https://api.weatherbit.io/v2.0/forecast/daily?"
    try :
        city_id = str(find_city_id(city_name))
        if(city_id == '0'):
            raise Exception('No exist City Name in City List')
    except Exception as e :
        print("Invalid City name")
        return passing_data
    city_id_url = "city_id=" + city_id
    key = "&key=" + ServiceKey

    api_url = url + city_id_url + key
    data = urllib.request.urlopen(api_url).read().decode('utf8')
    data_json = json.loads(data)
    parsed_json = data_json['data']
    
    for i in parsed_json:
        if i['datetime'] == forecast_date:
            passing_data['WSD'] = i['wind_spd']
            passing_data['TEMP'] = i['temp']
            passing_data['MAX'] = i['max_temp']
            passing_data['MIN'] = i['min_temp']
            passing_data['REH'] = i['rh']
            passing_data['POP'] = i['pop']
            passing_data['PRE'] = i['precip']

    t = passing_data['TEMP']
    v = passing_data['WSD']
    t = float(t)
    v = float(v)

    # 체감 온도 계산
    wci = getWCI(t, v)
    wci = round(wci, 2)

    t_high = passing_data['MAX']
    t_min = passing_data['MIN']
    t_high = float(t_high)
    t_min = float(t_min)

    wci_high = getWCI(t_high, v)
    wci_high = round(wci_high, 2)
    wci_low = getWCI(t_min, v)
    wci_low = round(wci_low, 2)

    passing_data['WCI'] = wci # current wind chill temp
    passing_data['WCIMAX'] = wci_high # maximum chill temp
    passing_data['WCIMIN'] = wci_low # minium chill temp

    return passing_data

# 체감 온도 구하기
def getWCI(temperature, wind_velocity): 
    """
     기온과 풍속을 입력 받아 체감온도를 반환한다.
     예시 : 12, 9.5
    """
    WCI = 13.12 + 0.6215 * temperature - 11.37 * math.pow(wind_velocity, 0.16) + 0.3965 * temperature * math.pow(wind_velocity, 0.16)
    return WCI
