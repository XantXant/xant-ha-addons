#!/usr/bin/env bashio

bashio::log.info "Get MQTT Data n..."

# if ! bashio::services.available "mqtt"; then
#    bashio::exit.nok "No internal MQTT Broker found. Please install Mosquitto broker."
# else
#     MQTT_HOST=$(bashio::services mqtt "host")
#     MQTT_PORT=$(bashio::services mqtt "port")
#     MQTT_USER=$(bashio::services mqtt "username")
#     MQTT_PASS=$(bashio::services mqtt "password")
#     bashio::log.info "Configured'$MQTT_HOST' mqtt broker."
#     echo "$MQTT_HOST $MQTT_PORT $MQTT_USER $MQTT_PASS" > /mqtt.txt
# fi
MQTT_HOST="juhu"
echo "$MQTT_HOST asdfS" > /mqtt.txt

python /app/main.py notest