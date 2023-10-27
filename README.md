# i2c-garage
Simple add-on to communicate via `i2c` with a relay board via mqtt.

This was developed for my needs, feel free to check it out!

**NOTE:** This addon needs to run with "Protection mode" turned off to access `/dev/i2c-1`.

## Notes
Board used: https://wiki.seeedstudio.com/Raspberry_Pi_Relay_Board_v1.0/

How to enable `i2c` on home assistant: https://community.home-assistant.io/t/add-on-hassos-i2c-configurator/264167

MQTT endpoint can be seen on the mqtt integration (I'm using [Mosquitto broker](https://github.com/home-assistant/addons/tree/master/mosquitto)).

I attached the board directly on my raspberry running home assistant.


Worth knowing some details about [MQTT QOS](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901103).

There are three possbile values:
* `0`: At most once delivery
* `1`: At least once delivery
* `2`: Exactly once delivery

In most case, when sending messages to this add-on, I'm using `2`!

Also, for future refrence, there are the i2cdetect and i2cset command do drive this board:
```bash
# Detect devices on `/dev/i2c-1`
i2cdetect -y -r 1

# Turn on only the first relay
i2cset -y 1 0x20 0x06 0xfe

# Turn off everything
i2cset -y 1 0x20 0x06 0xff
```

## How To
The simplest way to create a quick and dirty addon is to create a new folder in the `/addons/` folder
of your Home Assistant and throw there the `config.yaml`, `Dockerfile` and `i2c-garage.py`.
Make sure to reload your store.

Remember than when updating the addon manually, changes will not be picked up automatically. You will need to
bump the version, go on your addons list, refresh them and update the new extension created.

This is what I was simply doing during development.
```bash
scp config.yaml Dockerfile i2c-garage.py ha:/addons/i2c-garage/
```

## Notes
Being my first addon, I struggled with a bunch of new-be problems. The biggest one being I wasn't able to get
the `SUPERVISOR_TOKEN` in my environment. After lot of digging I realized your app is supposed to be called
from the `#!/usr/bin/with-contenv` env.

In my case, being just a simple python script, I set the shebang of my script to
```
#!/usr/bin/with-contenv python
```

And, rather than having `CMD [ "python3", "/i2c-garage.py" ]` in my `Dockerfile` I made executed the script directly
after making it executable:
```Dockefile
COPY i2c-garage.py /

RUN chmod a+x ./i2c-garage.py
CMD [ "./i2c-garage.py" ]
```
