import datetime
from django.conf import settings
import json
import math
import urllib
import pprint
from urllib.request import urlopen


ServiceKey = settings.GLOBAL_WEATHER_API_KEY

def find_city_id(city_name):
    with open('apps/api/locations/cities.list.json') as json_file:
    json_data = json.load(json_file)
    city_id = 0

    for i in json_data:
        if i['name'] = city_name:
            city_id = i['id']
        break
    print(city_id)
    return city_id


def get_weather_date(forecast_date, city_name): 
    """
     16일 이내 날짜와 도시를 입력받아 날씨정보를 반환한다.
     예시 input_date : 2020-03-31, city_name : "city_name" location index
    """
    with open('apps/api/locations/cities.list.json') as json_file:
        json_data = json.load(json_file)

    url = "https://api.weatherbit.io/v2.0/forecast/daily?"
    city_id = "city_id=" + find_city_id(city_name)
    key = "&key=" + ServiceKey

    api_url = url + city_id + key
    data = urllib.request.urlopen(api_url).read().decode('utf8')
    try :  
        data_json = json.loads(data)
        print(data_json)
    # get date and time
    
    parsed_json = data_json['data']
    print(prased_json)
    passing_data = {}
    
    for i in parsed_json:
        if i['datetime'] == forecast_date:
            passing_data['WSD'] = i['wind_spd']
            passing_data['TEMP'] = i['temp']
            passing_data['TMX'] = i['max_temp']
            passing_data['TMN'] = i['min_temp']
            passing_data['REH'] = i['rh']
            passing_data['POP'] = i['pop']
            passing_data['PRE'] = i['precip']

    print(passing_data)

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

# 체감 온도 구하기
def getWCI(temperature, wind_velocity): 
    """
     기온과 풍속을 입력 받아 체감온도를 반환한다.
     예시 : 12, 9.5
    """
    WCI = 13.12 + 0.6215 * temperature - 11.37 * math.pow(wind_velocity, 0.16) + 0.3965 * temperature * math.pow(wind_velocity, 0.16)
 
    return WCI