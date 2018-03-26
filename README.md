# WLSNK

> Wireless Sensor Networks

## Prerequisites

- MQTT Broker
- MultiConnect®mDot™ Developer Kit
  - My Model: MTUDK2-ST-MDOT
- Python 3

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

# after-zip/: try one time
# after-7z/: always retry

python m.py #main
# Result will be in the testData/ directory.
```
