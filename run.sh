#!/usr/bin/with-contenv bashio

echo "Create virtual environment"
mkdir /virtual_env
python3 -m venv /virtual_env
source /virtual_env/bin/activate

# echo "Install packages"
# python3 -m pip install smbus2
python3 -m pip install paho-mqtt smbus2 requests pyserial

echo "Start i2c-garage"
python3 i2c-garage.py
