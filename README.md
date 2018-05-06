# WLSNK

> Wireless Sensor Networks

## Prerequisites

- MQTT Broker
- MultiConnect®mDot™ Developer Kit
    - My Model: MTUDK2-ST-MDOT
- Python 3
    - requests
    - matplotlib

## Build

```
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
deactivate

pip freeze > requirements.txt
```

## 0326-LAB-2-Data-collect

```
pip install pyserial requests

# after-zip/: try one time (today, 2018/03/26)
# after-7z/: always retry (next week, 2018/04/02)

python m.py #main
# Result will be in the testData/ directory. Make sure you already have this folder before running.
```
