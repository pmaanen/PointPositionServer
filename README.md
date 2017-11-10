# PointPositionServer
Sends the position of a point in a canvas to a network socket

* Usage

```
usage: server.py [-h] [--port PORT] [--verbose] [--suppress-newline]
                 [--rate RATE]

Remote control for ... something. Works by sending the coordinates of the
point to the network.

optional arguments:
  -h, --help          show this help message and exit
  --port PORT         Specify the source port the server should use, subject
                      to privilege restrictions and availability.
  --verbose           Turn on extra verbosity
  --suppress-newline  Supress newline character at end of sent string
  --rate RATE         Set repetition rate in RATE seconds of position sender.
```

On another terminal you can connect via e.g. netcat:
```
nc 127.0.0.1 5551
```
