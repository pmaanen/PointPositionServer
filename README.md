# PointPositionServer
Sends the position of a point in a canvas to a network socket

* Usage

```
python server.py -h
usage: server.py [-h] [--port PORT] [--verbose]

Remote control for ... something. Works by sending the coordinates of the
point to the network.

optional arguments:
  -h, --help   show this help message and exit
  --port PORT  Specifies the source port the server should use, subject to
               privilege restrictions and availability.
  --verbose    Turns on extra verbosity.
```

On another terminal you can connect via e.g. netcat:
```
nc 127.0.0.1 5551
```
