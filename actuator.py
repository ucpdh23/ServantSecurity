import threading
from queue import Queue
import time

from picamera import PiCamera
from time import sleep

class Actuator:
    def __int__(self):
        print("creating items...")
        self.devices = {}


    def __processor(self):
        print()


    def __processAction(self, device, item):
        print("process", device, item)
        if item == 'BUTTONOFF':
            camera = PiCamera()
            camera.start_recording('recorded.h264')
            time.sleep(10)
            camera.stop_recording()
        print("processed", device, item)


    def addItem(self, device, action):
        if device not in self.devices:
            ts = time.time()
            event = {
                'action': "-",
                'firstEvent': ts,
                'lastEvent' : ts
            }
        else:
            event = self.devices[device]

        print("time", time.time())
        if event['action'] != action or event['lastEvent'] < time.time() - 60:
            print('event.action', event['action'])
            if event['action'] == action:
                first_ts = event['firstEvent']
            else:
                first_ts = time.time()

            self.devices[device] = {
                'action': action,
                'firstEvent': first_ts,
                'lastEvent': time.time()
            }

            self.__processAction(device, action)