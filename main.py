#! /bin/python
at = 'o.se1YZX6plVhVE84GqAOno53T5mw3MjDL'
from websocket import create_connection
import time, json
import mysql.connector as mariadb
mariadb_connection = mariadb.connect(user='spyai', password='bazinga', database='spyai')
cursor = mariadb_connection.cursor()



class Pushparser:

    def parse(self, obj):
        parsedJson = json.loads(obj)
        type = parsedJson['type']
        appName = ''
        sender = ''
        body = ''

        if type == 'push':
            pushData = parsedJson['push']
            pushType = pushData.get('type', None)


            if pushType == 'mirror':
                appName = pushData.get('application_name', None)
                sender = pushData.get('title', None)
                body = pushData.get('body', None)
                print('%s Message received from user: %s with text: %s' % (appName, sender, body))

            elif pushType == 'sms_changed':
                appName = 'sms'
                sender = pushData['notifications'][0].get('title', None)
                body = pushData['notifications'][0].get('body', None)
                print('%s Message received from user: %s with text: %s' % ('sms', sender, body))

            else:
                print('new event : %s' % pushType)
                print(parsedJson)

            queryStr = 'insert into data_bin (CONTACT_NAME, MSG_TEXT, APP) VALUES ({}, {}, {})'.format(sender,body,appName)
            cursor.execute(queryStr)

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
