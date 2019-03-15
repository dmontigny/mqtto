#!/usr/bin/env python3

# http://www.steves-internet-guide.com/into-mqtt-python-client/

import paho.mqtt.client as mqtt
from socket import gethostname
from clssubs import ClassSub

# This is the Subscriber

sub1 = ClassSub()
sub1.configure_logger()

rc = sub1.run('dave1')
print("rc: "+str(rc))

# sub1.connect('dave1')
# sub1.subscribe("durney/test")
# sub1.publish("durney/test", "Hi dave2")
#
# sub1.on_connect = sub1.on_connect
# sub1.on_message = sub1.on_message



