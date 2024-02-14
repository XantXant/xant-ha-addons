import datetime
from urllib.request import urlopen 
import json

class Forecastsolar:
    def __init__(self, lat, lon, dec, az, kwp, test=False):
        self.test = test
        self.url = f"https://api.forecast.solar/estimate/{lat:.4f}/{lon:.4f}/{dec}/{az}/{kwp}"
        print(self.url)
        self.time_of_data = datetime.datetime.now()
        self.time_to_get_new_data = datetime.datetime.now() - datetime.timedelta(hours=1)
        self.getNewData()

    def getNewData(self):
        act_time = datetime.datetime.now()
        if act_time > self.time_to_get_new_data:
            self.time_of_data = act_time
            self.time_to_get_new_data = self.time_of_data + datetime.timedelta(hours=2)

            if self.test is True:
                self.data = {'result': {'watts': {'2023-11-24 07:22:18': 0, '2023-11-24 08:00:00': 424, '2023-11-24 09:00:00': 427, '2023-11-24 10:00:00': 502, '2023-11-24 11:00:00': 555, '2023-11-24 12:00:00': 510, '2023-11-24 13:00:00': 462, '2023-11-24 14:00:00': 353, '2023-11-24 15:00:00': 197, '2023-11-24 16:00:00': 24, '2023-11-24 16:17:17': 0, '2023-11-25 07:23:41': 0, '2023-11-25 08:00:00': 2271, '2023-11-25 09:00:00': 1075, '2023-11-25 10:00:00': 928, '2023-11-25 11:00:00': 845, '2023-11-25 12:00:00': 733, '2023-11-25 13:00:00': 466, '2023-11-25 14:00:00': 357, '2023-11-25 15:00:00': 200, '2023-11-25 16:00:00': 25, '2023-11-25 16:16:30': 0}, 'watt_hours_period': {'2023-11-24 07:22:18': 0, '2023-11-24 08:00:00': 133, '2023-11-24 09:00:00': 426, '2023-11-24 10:00:00': 465, '2023-11-24 11:00:00': 529, '2023-11-24 12:00:00': 533, '2023-11-24 13:00:00': 486, '2023-11-24 14:00:00': 408, '2023-11-24 15:00:00': 275, '2023-11-24 16:00:00': 111, '2023-11-24 16:17:17': 3, '2023-11-25 07:23:41': 0, '2023-11-25 08:00:00': 687, '2023-11-25 09:00:00': 1673, '2023-11-25 10:00:00': 1002, '2023-11-25 11:00:00': 887, '2023-11-25 12:00:00': 789, '2023-11-25 13:00:00': 600, '2023-11-25 14:00:00': 412, '2023-11-25 15:00:00': 279, '2023-11-25 16:00:00': 113, '2023-11-25 16:16:30': 3}, 'watt_hours': {'2023-11-24 07:22:18': 0, '2023-11-24 08:00:00': 133, '2023-11-24 09:00:00': 559, '2023-11-24 10:00:00': 1024, '2023-11-24 11:00:00': 1553, '2023-11-24 12:00:00': 2086, '2023-11-24 13:00:00': 2572, '2023-11-24 14:00:00': 2980, '2023-11-24 15:00:00': 3255, '2023-11-24 16:00:00': 3366, '2023-11-24 16:17:17': 3369, '2023-11-25 07:23:41': 0, '2023-11-25 08:00:00': 687, '2023-11-25 09:00:00': 2360, '2023-11-25 10:00:00': 3362, '2023-11-25 11:00:00': 4249, '2023-11-25 12:00:00': 5038, '2023-11-25 13:00:00': 5638, '2023-11-25 14:00:00': 6050, '2023-11-25 15:00:00': 6329, '2023-11-25 16:00:00': 6442, '2023-11-25 16:16:30': 6445}, 'watt_hours_day': {'2023-11-24': 3369, '2023-11-25': 6445}}, 'message': {'code': 0, 'type': 'success', 'text': '', 'pid': 'c28G5o8Y', 'info': {'latitude': 48.0296, 'longitude': 14.1962, 'distance': 0, 'place': 'Kaipstraße 11, 4540 Pfarrkirchen bei Bad Hall, Austria', 'timezone': 'Europe/Vienna', 'time': '2023-11-24T16:58:45+01:00', 'time_utc': '2023-11-24T15:58:45+00:00'}, 'ratelimit': {'period': 3600, 'limit': 12, 'remaining': 6}}}
            else:
                webdata = urlopen(self.url)
                self.data = json.loads(webdata.read())
            # print(self.data)
            self.whd = []
            for elem in self.data['result']['watt_hours_day']:
                self.whd.append(self.data['result']['watt_hours_day'][elem])
    
    def getLocation(self):
        self.getNewData()
        return self.data['message']['info']['place']

    def getForecastsolarToday(self):
        self.getNewData()
        return self.whd[0]
    
    def getForecastsolarTomorrow(self):
        self.getNewData()
        return self.whd[1]

if __name__ == "__main__":
    latitude = 48.037222
    longitude = 14.416944
    declination = 24
    azimuth = -45
    modules_power = (410 * 35) / 1000

    print("latitude   : ", latitude)
    print("longitude  : ", longitude)
    print("declination: ", declination)
    print("azimuth    : ", modules_power)

    fc = Forecastsolar(latitude, longitude, declination, azimuth, modules_power, True)
    fc_today = fc.getForecastsolarToday()
    fc_tomorrow = fc.getForecastsolarTomorrow()
    print(f'Forcast Today: {fc_today:5} Tomorrow: {fc_tomorrow:5}')
    print(fc.getLocation())