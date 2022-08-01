import sys
import serial
from actuator import Actuator


def principal():
    actuator = Actuator()

    _serial = serial.Serial(
        port= '/dev/ttyAMA0',
        baudrate = 9600,
        timeout=5
    )

    while True:
        x = _serial.readline()
        parts = x.plit(b'\x00')
        for part in parts:
            action = part.decode()
            if action != "":
                actuator.addItem(action[:3], action[3:])


if __name__ == '__main__':
    principal()

