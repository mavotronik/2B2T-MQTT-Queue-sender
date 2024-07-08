# 2B2T-MQTT-Queue-sender
Short script sends your position in queue to MQTT broker

## Dependencies
```
pip3 install paho-mqtt
```

## Configuration (in `main.py`)
```
log_file = 'C:/Users/YOUR_USERNAME/AppData/Roaming/.minecraft/logs/latest.log' # put here your real path of `latest.log`

port = 1883 # set custom port or leave it as default
client_id = '2b2t-script'

broker = 'YOUR_BROKER_IP' # put here real ip of your mqtt broker
username = 'USERNAME' # put here your broker login or leave empty if not necessary
password = 'PASSWORD' # put here your broker password or leave empty if not necessary
base_topic = '2b2t' # put here needed topic or leave it as default
```
