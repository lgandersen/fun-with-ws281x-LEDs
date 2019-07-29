# fun-with-ws281x-LEDs
My small library for controlling ws281x LEDs with a raspberry pi.
The following packages are required:

    * numpy
    * rpi_ws281x
    * matplotlib

## script as service
Turning the script into a service that starts automatically when the
raspberry pi boots up can be done as follows (using systemd):

Copy the systemd unit-file in the `systemd` folder from this repository
into `/lib/systemd/system/` and make sure it has the right permissions set:

```
$ sudo cp ./systemd/led-controller.service /lib/systemd/system/
$ sudo chmod 644 /lib/systemd/system/led-controller.service
```

and enable it with `systemctl`:

```
$ sudo systemctl daemon-reload
$ sudo systemctl enable led-controller.service
```

and voila! It should snart execute `script.py` on startup using your
configuration etc. It can be stopped/started as follows:

```
pi@raspberrypi:~ $ sudo systemctl stop led-controller.service
pi@raspberrypi:~ $ sudo systemctl start led-controller.service
```
