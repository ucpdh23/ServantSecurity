import time
import logging

class Actuator:
    def __init__(self, eventBus):
        logging.info("creating actuator...")
        self.devices = {}
        self.eventBus = eventBus

    def __processor(self):
        print()

    def __processAction(self, device, item):
        logging.info("sending into the bus: %s %s", device, item)
        self.eventBus.send("event", body={'source': 'python', 'action': '_EVENT_', 'bean': { 'name':'door', 'status': item }})
        logging.info("sent into the bus: %s %s", device, item)


    def addItem(self, device, action):
        logging.info("AddItem...")
        if device not in self.devices:
            ts = time.time()
            event = {
                'action': "-",
                'firstEvent': ts,
                'lastEvent' : ts
            }
        else:
            event = self.devices[device]

        logging.info("time: %s", time.time())
        if event['action'] != action or event['lastEvent'] < time.time() - 60:
            logging.info('event.action: %s', event['action'])
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
        else:
            logging.info("rejecting event: %s", action)
