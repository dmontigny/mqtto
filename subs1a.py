#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from socket import gethostname

# This is the Subscriber
ping = 'dave1'
pong = 'dave2'
sub =  "durney/test"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("topic/test")


def on_message(client, userdata, msg):
    msg = msg.payload.decode()
    # print('incoming:', msg)
    # print(msg[:6], '*{}:*'.format(ping))
    if msg[:6] == '{}:'.format(ping):
        cmd = msg[7:]
        if cmd == 'ping me':
            print('{} ponging {}'.format(ping, pong))
            client.publish(sub, '{}: pong me'.format(pong))
        elif cmd == 'pong me':
            print('{} punging {}'.format(ping, pong))
            client.publish(sub, '{}: pung me'.format(pong))
        elif cmd == 'pung me':
            client.publish(sub, '{} punged!'.format(ping))
    elif msg[5] == ':':
        print('not my message', msg)
        pass
    else:
        print('message: ', msg)
        client.disconnect()

client = mqtt.Client(ping)
# client.connect('kermit', 1883, 60) if gethostname() == 'davelx' \
#     else client.connect('us1701', 1883, 60)

client.connect('52.0.117.162', 1883, 60)

client.subscribe(sub)
client.publish(sub, '{}: ping me'.format(pong))

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()