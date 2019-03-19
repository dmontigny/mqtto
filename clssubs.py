#!/usr/bin/env python3

# http://www.steves-internet-guide.com/into-mqtt-python-client/

import logging, sys
from os import path, remove
import paho.mqtt.client as mqtt

# This is the Subscriber

class ClassSub():
    def __init__(self, clientid = None):
        self._mqttc = mqtt.Client(clientid)
        self.logname = path.basename(sys.argv[0][:-3]) + '.log'
        self.logger = None
        self._mqttc.on_message = self.mqtt_on_message
        self._mqttc.on_connect = self.mqtt_on_connect
        self._mqttc.on_publish = self.mqtt_on_publish
        self._mqttc.on_subscribe = self.mqtt_on_subscribe
        self.subname = None
        self.client = None
        self.topic = None
        self.msg = None

    def connect(self, sub_name):
        from socket import gethostname
        self.logger.info('attempting connection')
        self.subname = sub_name
        self.client = mqtt.Client(self.subname)

        self.client.connect('52.0.117.162', 1883, 60)

        # self.client.connect('kermit', 1883, 60) if gethostname() == 'davelx' \
        #     else self.client.connect('us1701', 1883, 60)

    def mqtt_on_connect(self, client, userdata, flags, rc):
        self.logger.info("connected with result code " + str(rc))
        print("connected with result code " + str(rc))
        # client.subscribe("topic/test")

    def subscribe(self, topic):
        self.logger.info("subscribing to: {}".format(topic))
        self.topic = topic
        self.client.subscribe(self.topic)

    def mqtt_on_subscribe(self, mqttc, obj, mid, granted_qos):
        self.logger.info("subscribed: "+str(mid)+" "+str(granted_qos))
        print("subscribed: "+str(mid)+" "+str(granted_qos))

    def publish(self, topic, msg):
        self.logger.info('publishing {} on topic {}'.format(msg, topic))
        self.topic = topic
        self.msg = msg
        self.client.publish(self.topic, self.msg)

    def mqtt_on_publish(self, client, userdata, msg):
        msg = msg.payload.decode()
        print(msg)

    def mqtt_on_message(self, client, userdata, msg):
        msg = msg.payload.decode()
        print(msg)
        if msg == "Hello world!":
            print("Yes!")
            client.disconnect()
        else:
            print('wrong message')

    def run(self, sub_name):
        self.logger.info('starting {}'.format(sub_name))
        # self.sub_name = sub_name
        self.connect(sub_name)
        self.subscribe("durney/test")
        self.publish("durney/test", "dave2: wait")
        print('{} checked in'.format('dave3'))

        rc = 0
        while rc == 0:
            rc = self._mqttc.loop()
        return rc

    def configure_logger(self):
        # If applicable, delete the existing log file as it is overwritten each time
        if path.isfile(self.logname):
            remove(self.logname)

        # Create the Logger
        self.logger = logging.getLogger(self.logname[:-4])
        self.logger.setLevel(logging.DEBUG)

        # Create the Handler for logging data to a file
        logger_handler = logging.FileHandler(self.logname)
        logger_handler.setLevel(logging.DEBUG)

        # Create a Formatter for formatting the log messages
        logger_formatter = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s')

        # Add the Formatter to the Handler
        logger_handler.setFormatter(logger_formatter)

        # Add the Handler to the Logger
        self.logger.addHandler(logger_handler)
        self.logger.info('logger configuration_complete!')


