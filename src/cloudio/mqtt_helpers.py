# -*- coding: utf-8 -*-

import time
import paho.mqtt.client as mqtt
import ssl

class MqttAsyncClient():
    """Mimic the behavior of the java.MqttAsyncClient class"""

    def __init__(self, host, clientId='', clean_session=True):
        self._isConnected = False
        self._host = host
        self.client = mqtt.Client(client_id=clientId, clean_session=clean_session)

        self.client.on_connect = self.onConnect

    def connect(self, username, password):
        self.client.username_pw_set(username, password=password)
        self.client.tls_insecure_set(True)  # True: No verification of the server hostname in the server certificate
        self.client.tls_set('/Users/sth/.config/cloud.io/ca.pem',    # CA certificate
               #             '/Users/sth/.config/cloud.io/devel-8725b7b47d85-cert.pem',  # Client private key
               #             '/Users/sth/.config/cloud.io/devel-8725b7b47d85-key.pem',   # Client certificate
                            tls_version=ssl.PROTOCOL_TLSv1,                     # ssl.PROTOCOL_TLSv1, ssl.PROTOCOL_TLSv1_2
                            ciphers=None)      # None, 'ALL', 'TLSv1.2', 'TLSv1.0'

        self.client.connect(self._host, port=8883)
        self.client.loop_start()
        time.sleep(1)   # Wait a bit for the callback onConnect to be called

    def isConnected(self):
        return self._isConnected

    def onConnect(self, client, userdata, flags, rc):
        if rc == 0:
            self._isConnected = True
            print 'Info: Connection to cloudio broker established.'
        else:
            if rc == 1:
                print 'Error: Connection refused - incorrect protocol version'
            elif rc == 2:
                print 'Error: Connection refused - invalid client identifier'
            elif rc == 3:
                print 'Error: Connection refused - server unavailable'
            elif rc == 4:
                print 'Error: Connection refused - bad username or password'
            elif rc == 5:
                print 'Error: Connection refused - not authorised'
            else:
                print 'Error: Connection refused - unknown reason'

            if rc != 3: # Expect for 'server unavailable'
                # Close application
                exit(0)

    def publish(self, topic, payload, qos, retain):
        self.client.publish(topic, payload, qos, retain)

class MqttConnectOptions():
    def __init__(self):
        self._username = ''
        self._password = ''