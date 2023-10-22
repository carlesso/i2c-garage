#!/usr/bin/env python

import json
import logging
import sys

from os import environ
from smbus2 import SMBus
from time import sleep
import paho.mqtt.client as mqtt


MQTT_SERVER = "core-mosquitto"
MQTT_PORT = 1883


# Setup logs. Note only logs to stderr will show up in HomeAssistant Log tab
logger = logging.getLogger("i2c-garage")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stderr)
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# Simulate pressing the button of the remote by turning on the relay, waiting .3 seconds, and turning it off
def toggle_remote():
    with SMBus(1) as bus:
        bus.write_byte_data(0x20, 0x06, 0xFD)
        sleep(0.3)
        bus.write_byte_data(0x20, 0x06, 0xFF)


# Callback for successful connection to MQTT
def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected with return code {rc}. Subscribing to '/i2c-garage' topic.")

    # Subscribe to the /i2c-garage topic. We subscribe in the on_connect callback
    # so we re-subscribe in case of reconnections
    client.subscribe("/i2c-garage")


# Callback for every message received, in which we toggle the remote.
def on_message(client, userdata, msg):
    logger.info(f"Message received on topic: {msg.topic}. Triggering remote button.")
    toggle_remote()


# Load username and password from the options.json file, and check we have them
with open("/data/options.json", "r") as options_file:
    options: dict[str, str] = json.loads(options_file.read())
if "username" not in options or "password" not in options:
    raise RuntimeError(
        "Both username and password need to be set in the configuration tab"
    )

# Creates the main client for MQTT, setting the callbacks and the credentials
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username=options["username"], password=options["password"])

logger.info(f"Connecting to {MQTT_SERVER}:{MQTT_PORT} and starting the daemon.")
# Connect to the server
client.connect(host=MQTT_SERVER, port=1883, keepalive=60)

# Runs the loop forever
client.loop_forever()
