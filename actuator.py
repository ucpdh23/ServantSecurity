import time

class Actuator:
    def __init__(self, eventBus):
        print("creating actuator...")
        self.devices = {}
        self.eventBus = eventBus

    def __processor(self):
        print()

    def __processAction(self, device, item):
        print("process", device, item)
        self.eventBus.send("event", body={'source': 'python', 'action': '_EVENT_', 'bean': { 'name':'door', 'status': item }})
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
        else:
            print("rejecting event:", action)