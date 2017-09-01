#! /bin/python
at = 'o.se1YZX6plVhVE84GqAOno53T5mw3MjDL'
from websocket import create_connection
import time, json
import mysql.connector


class Pushparser:
    def parse(self, obj):
        parsedJson = json.loads(obj)
        type = parsedJson['type']

        if type == 'push':
            pushData = parsedJson['push']
            pushType = pushData.get('type', None)


            if pushType == 'mirror':
                appName = pushData.get('application_name', None)
                title = pushData.get('title', None)
                body = pushData.get('body', None)
                print('%s Message received from user: %s with text: %s' % (appName, title, body))

            elif pushType == 'sms_changed':
                title = pushData['notifications'][0].get('title', None)
                body = pushData['notifications'][0].get('body', None)
                print('%s Message received from user: %s with text: %s' % ('sms', title, body))

            else:
                print('new event : %s' % pushType)
                print(parsedJson)

        elif type == 'nop':
            print('new event : keepalive')

        else:
            print('cannot parse object')

ws = create_connection("wss://stream.pushbullet.com/websocket/" + at)
prsr = Pushparser()
try:
    while True:
        result = ws.recv()
        if result:
            prsr.parse(result)
        time.sleep(1)
except KeyboardInterrupt:
    print('interrupted!')

ws.close()
