import datetime
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
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
            self.time_to_get_new_data = self.time_of_data + datetime.timedelta(hours=3)

            if self.test is True:
                self.data = {'result': {'watts': {'2023-11-24 07:22:18': 0, '2023-11-24 08:00:00': 0, '2023-11-24 09:00:00': 0, '2023-11-24 10:00:00': 0, '2023-11-24 11:00:00': 0, '2023-11-24 12:00:00': 0, '2023-11-24 13:00:00': 0, '2023-11-24 14:00:00': 0, '2023-11-24 15:00:00': 0, '2023-11-24 16:00:00': 0, '2023-11-24 16:17:17': 0, '2023-11-25 07:23:41': 0, '2023-11-25 08:00:00': 0, '2023-11-25 09:00:00': 0, '2023-11-25 10:00:00': 0, '2023-11-25 11:00:00': 0, '2023-11-25 12:00:00': 0, '2023-11-25 13:00:00': 0, '2023-11-25 14:00:00': 0, '2023-11-25 15:00:00': 0, '2023-11-25 16:00:00': 0, '2023-11-25 16:16:30': 0}, 'watt_hours_period': {'2023-11-24 07:22:18': 0, '2023-11-24 08:00:00': 0, '2023-11-24 09:00:00': 0, '2023-11-24 10:00:00': 0, '2023-11-24 11:00:00': 0, '2023-11-24 12:00:00': 0, '2023-11-24 13:00:00': 0, '2023-11-24 14:00:00': 0, '2023-11-24 15:00:00': 0, '2023-11-24 16:00:00': 0, '2023-11-24 16:17:17': 0, '2023-11-25 07:23:41': 0, '2023-11-25 08:00:00': 0, '2023-11-25 09:00:00': 0, '2023-11-25 10:00:00': 0, '2023-11-25 11:00:00': 0, '2023-11-25 12:00:00': 0, '2023-11-25 13:00:00': 0, '2023-11-25 14:00:00': 0, '2023-11-25 15:00:00': 0, '2023-11-25 16:00:00': 0, '2023-11-25 16:16:30': 0}, 'watt_hours': {'2023-11-24 07:22:18': 0, '2023-11-24 08:00:00': 0, '2023-11-24 09:00:00': 0, '2023-11-24 10:00:00': 0, '2023-11-24 11:00:00': 0, '2023-11-24 12:00:00': 0, '2023-11-24 13:00:00': 0, '2023-11-24 14:00:00': 0, '2023-11-24 15:00:00': 0, '2023-11-24 16:00:00': 0, '2023-11-24 16:17:17': 0, '2023-11-25 07:23:41': 0, '2023-11-25 08:00:00': 0, '2023-11-25 09:00:00': 0, '2023-11-25 10:00:00': 0, '2023-11-25 11:00:00': 0, '2023-11-25 12:00:00': 0, '2023-11-25 13:00:00': 0, '2023-11-25 14:00:00': 0, '2023-11-25 15:00:00': 0, '2023-11-25 16:00:00': 0, '2023-11-25 16:16:30': 0}, 'watt_hours_day': {'2023-11-24': 0, '2023-11-25': 0}}, 'message': {'code': 0, 'type': 'success', 'text': '', 'pid': 'c28G5o8Y', 'info': {'latitude': 48, 'longitude': 14, 'distance': 0, 'place': 'Straße 1, 1234 Dorf, Austria', 'timezone': 'Europe/Vienna', 'time': '2023-11-24T16:58:45+01:00', 'time_utc': '2023-11-24T15:58:45+00:00'}, 'ratelimit': {'period': 3600, 'limit': 12, 'remaining': 6}}}
            else:
                self.data = {'result': {'watts': {'2023-11-24 07:22:18': 0, '2023-11-24 08:00:00': 0, '2023-11-24 09:00:00': 0, '2023-11-24 10:00:00': 0, '2023-11-24 11:00:00': 0, '2023-11-24 12:00:00': 0, '2023-11-24 13:00:00': 0, '2023-11-24 14:00:00': 0, '2023-11-24 15:00:00': 0, '2023-11-24 16:00:00': 0, '2023-11-24 16:17:17': 0, '2023-11-25 07:23:41': 0, '2023-11-25 08:00:00': 0, '2023-11-25 09:00:00': 0, '2023-11-25 10:00:00': 0, '2023-11-25 11:00:00': 0, '2023-11-25 12:00:00': 0, '2023-11-25 13:00:00': 0, '2023-11-25 14:00:00': 0, '2023-11-25 15:00:00': 0, '2023-11-25 16:00:00': 0, '2023-11-25 16:16:30': 0}, 'watt_hours_period': {'2023-11-24 07:22:18': 0, '2023-11-24 08:00:00': 0, '2023-11-24 09:00:00': 0, '2023-11-24 10:00:00': 0, '2023-11-24 11:00:00': 0, '2023-11-24 12:00:00': 0, '2023-11-24 13:00:00': 0, '2023-11-24 14:00:00': 0, '2023-11-24 15:00:00': 0, '2023-11-24 16:00:00': 0, '2023-11-24 16:17:17': 0, '2023-11-25 07:23:41': 0, '2023-11-25 08:00:00': 0, '2023-11-25 09:00:00': 0, '2023-11-25 10:00:00': 0, '2023-11-25 11:00:00': 0, '2023-11-25 12:00:00': 0, '2023-11-25 13:00:00': 0, '2023-11-25 14:00:00': 0, '2023-11-25 15:00:00': 0, '2023-11-25 16:00:00': 0, '2023-11-25 16:16:30': 0}, 'watt_hours': {'2023-11-24 07:22:18': 0, '2023-11-24 08:00:00': 0, '2023-11-24 09:00:00': 0, '2023-11-24 10:00:00': 0, '2023-11-24 11:00:00': 0, '2023-11-24 12:00:00': 0, '2023-11-24 13:00:00': 0, '2023-11-24 14:00:00': 0, '2023-11-24 15:00:00': 0, '2023-11-24 16:00:00': 0, '2023-11-24 16:17:17': 0, '2023-11-25 07:23:41': 0, '2023-11-25 08:00:00': 0, '2023-11-25 09:00:00': 0, '2023-11-25 10:00:00': 0, '2023-11-25 11:00:00': 0, '2023-11-25 12:00:00': 0, '2023-11-25 13:00:00': 0, '2023-11-25 14:00:00': 0, '2023-11-25 15:00:00': 0, '2023-11-25 16:00:00': 0, '2023-11-25 16:16:30': 0}, 'watt_hours_day': {'2023-11-24': 0, '2023-11-25': 0}}, 'message': {'code': 0, 'type': 'success', 'text': '', 'pid': 'c28G5o8Y', 'info': {'latitude': 48, 'longitude': 14, 'distance': 0, 'place': 'Straße 1, 1234 Dorf, Austria', 'timezone': 'Europe/Vienna', 'time': '2023-11-24T16:58:45+01:00', 'time_utc': '2023-11-24T15:58:45+00:00'}, 'ratelimit': {'period': 3600, 'limit': 12, 'remaining': 6}}}
                try:
                    webdata = urlopen(self.url)
                except HTTPError as e:
                    print("Forecast: HTTPError: ", e.code)
                except URLError as e:
                    print("Forecast: URLError: ", e.reason)
                except ValueError:
                    print("Forecast: ValueError")
                except TypeError:
                    print("Forecast: TypeError")
                except OSError:
                    print("Forecast: OSError")
                else:
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

    print("latitude     : ", latitude)
    print("longitude    : ", longitude)
    print("declination  : ", declination)
    print("azimuth      : ", azimuth)
    print("modules_power: ", modules_power)

    fc = Forecastsolar(latitude, longitude, declination, azimuth, modules_power, True)
    fc_today = fc.getForecastsolarToday()
    fc_tomorrow = fc.getForecastsolarTomorrow()
    print(f'Forcast Today: {fc_today:5} Tomorrow: {fc_tomorrow:5}')
    print(fc.getLocation())