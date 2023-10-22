ARG BUILD_FROM
FROM $BUILD_FROM

# The core of the addon is a python script, so we install python
# and the dependencies we need.
RUN apk add --no-cache python3 py3-pip
RUN pip3 install --no-cache-dir paho-mqtt smbus2

COPY i2c-garage.py /
CMD [ "python3", "/i2c-garage.py" ]