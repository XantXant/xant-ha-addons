import datetime
import sys
import time
from forecastsolar import Forecastsolar
from gen24 import Gen24
from awattarcharge import Awattar
from regeln import getstartendtime
import functools
import json
import os
import paho.mqtt.client as mqtt

print = functools.partial(print, flush=True)

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"MQTT Failed to connect: {reason_code}")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe("$SYS/#")
        print("MQTT Connected!")

if __name__ == "__main__":
    istest = True
    host = "192.168.1.178"
    latitude = 48.037222
    longitude = 14.416944
    declination = 24
    azimuth = -45
    modules_power = (410 * 35) / 1000
    rule_charge = True
    rule_charge_start_hour = 20
    rule_charge_end_hour = 6
    rule_charge_hours_count = 3
    rule_charge_hours_power = [2000, 1500, 1000]
    max_soc = True
    max_soc_value = 80

    print(sys.argv[0])
    print(sys.argv[1])
    print(sys.argv[2])
    print(sys.argv[3])
    print(sys.argv[4])
    mqtt_host = sys.argv[1]
    mqtt_port = int(sys.argv[2])
    print(mqtt_port, type(mqtt_port))
    mqtt_user = sys.argv[3]
    mqtt_pass = sys.argv[4]

    if len(sys.argv) == 5:
        # print(os.listdir("/"))
        # print(os.listdir("/data/"))
        
        # with open("/data/mqtt.txt") as mfile:
        #     print(mfile.readlines())
        #     mfile.close()

        with open("/data/options.json") as file:
            istest = False

            os.environ['TZ'] = 'Europe/Vienna'
            time.tzset()

            data = json.load(file)

            print(data)

            host = data["gen24_ip_dns"]
            latitude = data["forecast_latitude"]
            longitude = data["forecast_longitude"]
            declination = data["forecast_declination"]
            azimuth = data["forecast_azimuth"]
            modules_power = data["forecast_modules_power"]
            rule_charge = data["rule_charge"]
            rule_charge_start_hour = data["rule_charge_start_hour"]
            rule_charge_end_hour = data["rule_charge_end_hour"]
            rule_charge_hours_count = data["rule_charge_hours_count"]
            rule_charge_hours_power = [data["rule_charge_hours_power_1"], data["rule_charge_hours_power_2"], data["rule_charge_hours_power_3"], data["rule_charge_hours_power_4"], data["rule_charge_hours_power_5"]]
            max_soc = data["max_soc"]
            max_soc_value = data["max_soc_value"]
    else:
        print(f"{' Test ':=^30}")

    print("")
    print(f"{' Init ':=^30}")
    print("latitude   : ", latitude)
    print("longitude  : ", longitude)
    print("declination: ", declination)
    print("azimuth    : ", azimuth)
    print("module kWp : ", modules_power)
    print("host       : ", host)
    print("-------------------------------------------------")
    print(f"Rule charge: {rule_charge}")
    if rule_charge:
        print(f"Start from {rule_charge_start_hour} until {rule_charge_end_hour} in the cheapest {rule_charge_hours_count} hours")
        for i, p in enumerate(rule_charge_hours_power[:rule_charge_hours_count]):
            print(f"{i+1}: {p}")
    print("-------------------------------------------------")

    fc = Forecastsolar(latitude, longitude, declination, azimuth, modules_power)
    gen24 = Gen24(host)
    tarif = Awattar(istest)

    print(f'Forecast location: {fc.getLocation()}')

    print("")
    print("-------------------------------------------------")
    if max_soc is True:
        print(f"Max SoC: {max_soc_value}")
        print("-------------------------------------------------")
    print("")
    print(f"{' Start ':=^30}")

    isCharging = False

    isMaxSoC = False

    last_hour = 55

    refreshcount = 0

    last_fc_today = 0
    last_fc_tomorrow = 0

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect

    mqttc.user_data_set([])
    mqttc.username_pw_set(mqtt_user, mqtt_pass)
    mqttc.connect(mqtt_host, mqtt_port)

    mqttc.loop_start()

    while mqttc.is_connected() is False:
        print("MQTT wait for connection...")
        time.sleep(5)

    mqttc.publish("homeassistant/sensor/batterycharge/config", '{ "name": "Battery SoC", "device_class": "battery", "state_topic": "batterycharge/state", "value_template": "{{ value_json.batterysoc }}", "unit_of_measurement": "%" }')

    try:
        while True:
            # MQTT
            mqttc.publish("batterycharge/state", f'{{ "batterysoc": {gen24.getSoC():.1f}}} ')
            
            # Forecast
            new_fc_today = fc.getForecastsolarToday()
            new_fc_tomorrow = fc.getForecastsolarTomorrow()
            if new_fc_today != last_fc_today or new_fc_tomorrow != last_fc_tomorrow:
                last_fc_today = new_fc_today
                last_fc_tomorrow = new_fc_tomorrow
                # print(f'Forecast Today: {last_fc_today:5} Tomorrow: {last_fc_tomorrow:5}')

            # Awattar
            tarif.getNewData()

            act_time = datetime.datetime.now()

            hour_changed = False

            if last_hour != act_time.hour:
                # nur ausgeben wenn eine neue Stunde angefangen hat
                last_hour = act_time.hour
                hour_changed = True

            if hour_changed:
                price_euro_p_mwh, price_cent_p_kwh = tarif.get_act_marcetprice(act_time.timestamp())
                print(f'{act_time.strftime("%d.%m.%Y %H:%M")} {price_euro_p_mwh:6.2f} Euro/MWh {price_cent_p_kwh:6.2f} Cent/kWh', end='')
                print(f' Forecast Today: {last_fc_today:6} Wh Tomorrow: {last_fc_tomorrow:6} Wh')

            act_tst = act_time.timestamp()
            start_tst, end_tst = getstartendtime(act_tst, rule_charge_start_hour, rule_charge_end_hour)

            ret = False
            price = 0
            if act_tst >= start_tst and act_tst < end_tst:
                ret, price_mwh, price_kwh, rank = tarif.isLowestPrice(act_tst, start_tst, end_tst, rule_charge_hours_count)
                if rank >= len(rule_charge_hours_power):
                    rank = 0

            if rule_charge is True:
                if ret is True:
                    if isCharging is False:
                        isCharging = True
                        gen24.chargeBattery(rule_charge_hours_power[rank])

                    if hour_changed:
                        print(f"{' Charge Battery ':=^30}", f'SoC {gen24.getSoC():.1f} % Price {price_mwh:.2f} Euro/MWh {price_kwh:.2f} Cent/kWh with max. {rule_charge_hours_power[rank]} W [{rank + 1}]')

                    # damit modbus (gen24) nicht ins timeout läuft
                    refreshcount += 1
                    if refreshcount > 5:
                        refreshcount = 0
                        gen24.chargeBattery(rule_charge_hours_power[rank])
                else:
                    if isCharging is True:
                        isCharging = False
                        print(f"{' Back to normal ':=^30}", "SoC", gen24.getSoC())
                        gen24.backToNormal()
            else:
                if max_soc is True:
                    if gen24.getSoC() >= max_soc_value:
                        gen24.getData()
                        if isMaxSoC is False:
                            isMaxSoC = True
                            print(f"{' Stop charging @ ':=^30}", "SoC", gen24.getSoC())
                        gen24.dischargeBattery(0)
                    else:
                        if isMaxSoC is True:
                            isMaxSoC = False
                            print(f"{' Back to normal ':=^30}", "SoC", gen24.getSoC())
                            gen24.backToNormal()

            time.sleep(60)
    except KeyboardInterrupt:
        print("Exit")

    mqttc.loop_stop()
