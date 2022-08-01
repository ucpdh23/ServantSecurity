import sys
import serial
from actuator import Actuator
import threading

import ConfigParser

from vertx import EventBus


def serial_processor(ebus):
    _serial = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        timeout=5
    )

    while True:
        x = _serial.readline()
        parts = x.split(b'\x00')
        for part in parts:
            action = part.decode()
            if action != "":
                ebus.send("event", body={'name': 'python', 'value': 'yes'})



def principal(configFile):
    config = ConfigParser.RawConfigParser()
    config.read(configFile)

    host = config['EventBus']['host']
    port = config['EventBus']['port']

    ebus = EventBus(host, port)
    ebus.connect()

    t = threading.threat(target= serial_processor, args=(ebus))
    t.start()



if __name__ == '__main__':
    principal(sys.argv[1])

