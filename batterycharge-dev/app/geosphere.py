from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import json
from datetime import datetime

warntypid = {1:"storm", 2:"rain", 3:"snow", 4:"black ice", 5:"thunderstorm", 6:"heat", 7:"cold"}
warnstufeid = {1:"yellow", 2:"orange", 3:"red"}

class Geosphere:
    def __init__(self, latitude, longitude) -> None:
        self.latitude = latitude
        self.longitude = longitude
        self.url = f"https://warnungen.zamg.at/wsapp/api/getWarningsForCoords?lon={longitude}&lat={latitude}&lang=de"
        # print(self.url)
        self.warnings = []
        self.getData()
    
    def getData(self):
        try:
            webdata = urlopen(self.url)
        except HTTPError as e:
            print("Geosphere: HTTPError: ", e.code)
        except URLError as e:
            print("Geosphere: URLError: ", e.reason)
        except ValueError:
            print("Geosphere: ValueError")
        except TypeError:
            print("Geosphere: TypeError")
        except OSError:
            print("Geosphere: OSError")
        else:
            self.data = json.loads(webdata.read())
            # print(self.data)
            self.warnings = []
            for warning in self.data["properties"]["warnings"]:
                self.warnings.append(warning["properties"])
                # print(warning["properties"])
    
    def printData(self):
        for index, warning in enumerate(self.warnings):
            print(f"{index:2}: {warntypid[warning["rawinfo"]["wtype"]]:13}", end="")
            print(f"{warnstufeid[warning["rawinfo"]["wlevel"]]:7}", end="")
            start = datetime.fromtimestamp(int(warning["rawinfo"]["start"]))
            end = datetime.fromtimestamp(int(warning["rawinfo"]["end"]))
            print(f"{start} - {end}")

if __name__ == "__main__":
    geo = Geosphere(48.030278, 14.199444)
    geo.printData()
