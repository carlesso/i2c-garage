ARG BUILD_FROM
FROM $BUILD_FROM

ARG TEMPIO_VERSION BUILD_ARCH

# The core of the addon is a python script, so we install python and pip
RUN apk add --no-cache python3 py3-pip

COPY i2c-garage.py /
COPY run.sh /

RUN chmod a+x ./run.sh
CMD [ "./run.sh" ]
