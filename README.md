# REST/MQTT-Proxy (Prototype)


## Run

`python main.py 
`
## Docker

`docker run -it \
    -e APP_CONFIG_FILE=/srv/rest-mqtt-proxy/config.ini \
    -e PRE_MAPPING_DIR=/srv/rest-mqtt-proxy/mappings \
    -v ./config.ini:/srv/rest-mqtt-proxy/config.ini:ro
    -v ./mappings/:/srv/rest-mqtt-proxy/mappings/:ro
    kungalex/http-mqtt-proxy:latest
`
## Publish MQTT

`mosquitto_pub -h iot.eclipse.org -p 1883 -m value -t test-a/topic/abc
`

## Curl

`curl -G 'http://localhost:8086/query?pretty=true' --data-urlencode "db=iot" --data-urlencode "q=SELECT last("float_value1") FROM "iot"."autogen"."topic""
`

## Influxdb
`SELECT mean("float_value") AS "mean_float_value" FROM "iot"."autogen"."test-a/topic/abc"
`
## TODO
- JWT-Auth 