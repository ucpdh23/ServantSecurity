import os
import sys
import serial
from actuator import Actuator
import threading
import time
import configparser

import logging

from vertx import EventBus
from picamera import PiCamera

import requests
import json


def do_record_video(info):
    with PiCamera() as camera:
        camera.start_recording('recorded.h264')
        time.sleep(int(info['body']['bean']['time']))
        camera.stop_recording()
        logging.info("finished recording")

    logging.info("transforming file")
    os.system('rm -rf /opt/security/recorded.mp4')
    os.system('ffmpeg -framerate 24 -i /opt/security/recorded.h264 -c copy /opt/security/recorded.mp4 -y -nostdin')
    logging.info("transformed file")

    url = "http://192.168.1.2:8989/security/video/" + info['body']['bean']['code']
    payload = {}
    files = [
        ('file', ('recorded.mp4', open(
            '/opt/security/recorded.mp4',
            'rb'), 'video/mp4'))
    ]
    headers = {}

    logging.info("sending video")
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    logging.info("sent video")

    logging.debug(response.text)


def handler(info):
    logging.info("Got message from server: %s" % info)

    if info['body']['action'] == 'RECORD_VIDEO':
        do_record_video(info)
    elif info['body']['action'] == 'SHUTDOWN_SECURITY':
        os.system('sudo shutdown now')
    else:
        logging.warning("Nothing to do with: %s" % info)


def serial_processor(ebus):
    logging.info("STARTED...")
    _serial = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        timeout=1
    )

    logging.info("Initializing Actuator...")
    _act = Actuator(ebus)

    logging.info("Starting infinite loop...")
    current_time = time.time()
    while True:
        x = _serial.readline()
        parts = x.split(b'\x00')
        for part in parts:
            action = part.decode()
            if action != "":
                _act.addItem(action[:3], action[3:])

        new_time = time.time()
        if new_time > current_time + 300:
            current_time = new_time
            output = os.popen('vcgencmd measure_temp').read()
            _act.addItem('RBP', output)

    logging.info("finished")


def principal(config):

    host = config['EventBus']['host']
    port = config['EventBus']['port']

    ebus = EventBus(host, int(port))
    logging.info("connecting to %s %s", host, int(port))
    ebus.connect()

    logging.info("handing actions...")
    logging.debug("...RECORD_VIDEO")
    ebus.register_handler("RECORD_VIDEO", handler)
    logging.debug("...SHUTDOWN_SECURITY")
    ebus.register_handler("SHUTDOWN_SECURITY", handler)


    t = threading.Thread(target= serial_processor, args=[ebus])
    t.start()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(sys.argv[1])

    logging.basicConfig(filename='/var/log/security.log',
                        level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

    principal(config)

