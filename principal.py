import os
import sys
import serial
from actuator import Actuator
import threading
import time
import configparser

from vertx import EventBus
from picamera import PiCamera

import requests
import json

camera = PiCamera()

def handler(info):
    print("Got message from server: %s" % info)
    #info = json.loads(msg)


    camera.start_recording('recorded.h264')
    time.sleep(int(info['body']['bean']['time']))
    camera.stop_recording()
    print("finished recording")

    print("transforming file")
    os.system('rm -rf recorded.mp4')
    os.system('MP4Box -add recorded.h264 recorded.mp4')
    print("transformed file")

    url = "http://192.168.1.2:8989/security/video/" + info['body']['bean']['code']
    payload = {}
    files = [
        ('file', ('recorded.mp4', open(
            'recorded.mp4',
            'rb'), 'video/mp4'))
    ]
    headers = {}


    print("sending video")
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print("sent video")

    print(response.text)


def serial_processor(ebus):
    print("started...")
    _serial = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        timeout=5
    )

    _act = Actuator(ebus)

    while True:
        x = _serial.readline()
        parts = x.split(b'\x00')
        for part in parts:
            action = part.decode()
            if action != "":
                _act.addItem(action[:3], action[3:])

    print("finished")


def principal(configFile):
    config = configparser.ConfigParser()
    config.read(configFile)

    host = config['EventBus']['host']
    port = config['EventBus']['port']

    ebus = EventBus(host, int(port))
    print("connecting to", host, int(port))
    ebus.connect()

    print("handing RECORD_VIDEO action...")
    ebus.register_handler("RECORD_VIDEO", handler)

    t = threading.Thread(target= serial_processor, args=[ebus])
    t.start()


if __name__ == '__main__':
    principal(sys.argv[1])

