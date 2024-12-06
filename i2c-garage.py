#!/usr/bin/with-contenv python

import logging
import requests
import sys

from os import environ
from serial import Serial
from time import sleep
import paho.mqtt.client as mqtt


# MQTT_SERVER = "core-mosquitto"
# MQTT_PORT = 1883


# Setup logs. Note only logs to stderr will show up in HomeAssistant Log tab
logger = logging.getLogger("i2c-garage")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stderr)
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# Load MQTT information from Supervisor API
headers = {
    "Authorization": f"Bearer {environ['SUPERVISOR_TOKEN']}",
    "content-type": "application/json",
}
response = requests.get("http://supervisor/services/mqtt", headers=headers)
data = response.json().get("data")
if not data:
    raise RuntimeError(
        f"Unable to fetch MQTT data from Supervisor API. Response: {response.content}"
    )


# Simulate pressing the button of the remote by turning on the relay, waiting .3 seconds, and turning it off
def toggle_remote():
    with Serial("/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0") as s:
        s.write([0xA0, 0x01, 0x01, 0xA2])
        sleep(0.3)
        s.write([0xA0, 0x01, 0x00, 0xA1])


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


# Creates the main client for MQTT, setting the callbacks and the credentials
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username=data["username"], password=data["password"])

logger.info(f"Connecting to {data['host']}:{data['port']} and starting the daemon.")
# Connect to the server
client.connect(host=data["host"], port=data["port"], keepalive=60)

# Runs the loop forever
client.loop_forever()
