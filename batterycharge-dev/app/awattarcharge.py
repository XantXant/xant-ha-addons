from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import json
import datetime
import functools

print = functools.partial(print, flush=True)

class Awattar:
    def __init__(self, test=False):
        self.test = test
        self.time_of_data = datetime.datetime.now()
        self.time_to_get_new_data = datetime.datetime.now() - datetime.timedelta(hours=1)
        self.getNewData()

    def getNewData(self):
        act_time = datetime.datetime.now()
        if act_time > self.time_to_get_new_data:
            self.time_of_data = act_time
            self.time_to_get_new_data = self.time_of_data + datetime.timedelta(hours=2)
            # self.time_to_get_new_data = self.time_of_data + datetime.timedelta(days=1)
            # self.time_to_get_new_data = self.time_to_get_new_data.replace(hour=14, minute=0)

            # end datum für abfrage -1 Tag
            url_date_start = self.time_of_data - datetime.timedelta(days=2)
            # end datum für abfrage +2 Tage
            url_date_end = self.time_of_data + datetime.timedelta(days=2)

            # print(f"{' Get new data from Awattar ':-^30}")
            if self.test is True:
                self.webdata = {'object': 'list', 'data': [{'start_timestamp': 1702116000000, 'end_timestamp': 1702119600000, 'marketprice': 103.65, 'unit': 'Eur/MWh'}, {'start_timestamp': 1702119600000, 'end_timestamp': 1702123200000, 'marketprice': 101.88, 'unit': 'Eur/MWh'}, {'start_timestamp': 1702123200000, 'end_timestamp': 1702126800000, 'marketprice': 103.31, 'unit': 'Eur/MWh'}, {'start_timestamp': 1702126800000, 'end_timestamp': 1702130400000, 'marketprice': 104.91, 'unit': 'Eur/MWh'}, {'start_timestamp': 1702130400000, 'end_timestamp': 1702134000000, 'marketprice': 109.26, 'unit': 'Eur/MWh'}, {'start_timestamp': 1702134000000, 'end_timestamp': 1702137600000, 'marketprice': 119.93, 'unit': 'Eur/MWh'}, {'start_timestamp': 1702137600000, 'end_timestamp': 1702141200000, 'marketprice': 107.24, 'unit': 'Eur/MWh'}, {'start_timestamp': 1702141200000, 'end_timestamp': 1702144800000, 'marketprice': 104.95, 'unit': 'Eur/MWh'}, {'start_timestamp': 1702144800000, 'end_timestamp': 1702148400000, 'marketprice': 94.37, 'unit': 'Eur/MWh'}, {'start_timestamp': 1702148400000, 'end_timestamp': 1702152000000, 'marketprice': 83.06, 'unit': 'Eur/MWh'}, {'start_timestamp': 1702152000000, 'end_timestamp': 1702155600000, 'marketprice': 73.1, 'unit': 'Eur/MWh'}, {'start_timestamp': 1702155600000, 'end_timestamp': 1702159200000, 'marketprice': 61.52, 'unit': 'Eur/MWh'}, {'start_timestamp': 1702159200000, 'end_timestamp': 1702162800000, 'marketprice': 46.18, 'unit': 'Eur/MWh'}], 'url': '/at/v1/marketdata'}
            else:
                self.webdata = {}
                url = f"https://api.awattar.at/v1/marketdata?start={int(url_date_start.timestamp()*1000)}&end={int(url_date_end.timestamp()*1000)}"
                # print(url)
                try:
                    webdata = urlopen(url)
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
                    self.webdata = json.loads(webdata.read())
                    # print(self.webdata)

            self.data = self.webdata['data']
            self.data_sorted = sorted(self.data, key=self.get_marketprice)
            # for elem in self.data_sorted:
            #     start = datetime.datetime.fromtimestamp(elem['start_timestamp']//1000)
            #     print(start, elem['marketprice']*1.2)
            return True
        else:
            return False
    
    def isLowestPrice(self, act, start, end, count):
        self.getNewData()

        # alle Preise in der Regelzeit
        rl = []
        for elem in self.data_sorted:
            elem_start = elem['start_timestamp'] // 1000
            if elem_start >= start and elem_start < end:
                rl.append(elem)
        
        # print("in timerange:")
        # for elem in rl:
        #     start = datetime.datetime.fromtimestamp(elem['start_timestamp']//1000)
        #     print(start, elem['marketprice']*1.2)

        # print("in cheapest:")
        # for elem in rl[0:count]:
        #     start = datetime.datetime.fromtimestamp(elem['start_timestamp']//1000)
        #     print(start, elem['marketprice']*1.2)
        
        # nur die günstingen count in Regelzeit
        price_mwh = 0
        price_kwh = 0
        act_in_range = False
        act_rank = 0
        for rank, elem in enumerate(rl[0:count]):
            elem_start = elem['start_timestamp'] // 1000
            elem_end = elem['end_timestamp'] // 1000
            # if newdata is True:
            #     print(datetime.datetime.fromtimestamp(elem_start), elem['marketprice'])
            if act >= elem_start and act < elem_end:
                act_in_range = True
                price_mwh, price_kwh = self.get_marketprice(elem)
                act_rank = rank
                break
        
        return act_in_range, price_mwh, price_kwh, act_rank

    def get_marketprice(self, item):
        price = item['marketprice']
        return price*1.2, price*1.2/10

    def get_act_marcetprice(self, tst):
        price = 0
        for elem in self.data_sorted:
            elem_start = elem['start_timestamp'] // 1000
            elem_end = elem['end_timestamp'] // 1000
            if tst >= elem_start and tst < elem_end:
                price = elem['marketprice']
                break
        return price*1.2, price*1.2/10

if __name__ == "__main__":
    print("awattar charge")
