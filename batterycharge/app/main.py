import datetime
import sys
import time
from forecastsolar import Forecastsolar
from gen24 import Gen24
from awattarcharge import Awattar
from regeln import getstartendtime
import functools
import json

print = functools.partial(print, flush=True)

if __name__ == "__main__":
    istest = True
    host = "192.168.1.178"
    latitude = 48.037222
    longitude = 14.416944
    declination = 24
    azimuth = -45
    modules_power = (410 * 35) / 1000

    if len(sys.argv) == 2:
        with open("/data/options.json") as file:
            istest = False

            data = json.load(file)

            host = data["gen24_ip_dns"]
            latitude = data["forecast_latitude"]
            longitude = data["forecast_longitude"]
            declination = data["forecast_declination"]
            azimuth = data["forecast_azimuth"]
            modules_power = data["forecast_modules_power"]

    print("")
    print(f"{' Init ':=^30}")
    print("latitude   : ", latitude)
    print("longitude  : ", longitude)
    print("declination: ", declination)
    print("azimuth    : ", azimuth)
    print("module kWp : ", modules_power)
    print("host       : ", host)
    print("-------------------------------------------------")

    fc = Forecastsolar(latitude, longitude, declination, azimuth, modules_power)
    gen24 = Gen24(host)
    tarif = Awattar(istest)

    print("")
    print(f"{' Start ':=^30}")

    rule_start_hour = 20
    rule_end_hour = 6
    rule_max_hours = 3
    rule_max_power = -5

    isCharging = False

    last_hour = 55

    refreshcount = 0

    try:
        while True:
            tarif.getNewData()

            act_time = datetime.datetime.now()

            if last_hour != act_time.hour:
                # nur ausgeben wenn eine neue Stunde angefangen hat
                last_hour = act_time.hour
                price_euro_p_mwh, price_cent_p_kwh = tarif.get_act_marcetprice(act_time.timestamp())
                print("act   ", act_time, "price", price_euro_p_mwh, "Euro/MWh", price_cent_p_kwh, "Cent/kWh")

            act_tst = act_time.timestamp()
            start_tst, end_tst = getstartendtime(act_tst, rule_start_hour, rule_end_hour)

            ret = False
            price = 0
            if act_tst >= start_tst and act_tst < end_tst:
                ret, price_mwh, price_kwh = tarif.isLowestPrice(act_tst, start_tst, end_tst, rule_max_hours)

            if ret is True:
                if isCharging is False:
                    isCharging = True
                    print(f"{' Charge Battery ':=^30}", "SoC", gen24.getSoC(), price_mwh, "Euro/MWh", price_kwh, "Cent/kWh")
                    gen24.chargeBattery(rule_max_power)

                # damit modbus (gen24) nicht ins timeout läuft
                refreshcount += 1
                if refreshcount > 5:
                    refreshcount = 0
                    gen24.chargeBattery(rule_max_power)
            else:
                if isCharging is True:
                    isCharging = False
                    print(f"{' Back to normal ':=^30}", "SoC", gen24.getSoC())
                    gen24.backToNormal()

            time.sleep(60)
    except KeyboardInterrupt:
        print("Exit")