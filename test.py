from __future__ import print_function
import csv
import serial
from time import sleep
import time 
from datetime import datetime
import paho.mqtt.publish as publish
import psutil
import ssl
import threading

useSSLWebsockets = True
mqttHost = "mqtt.thingspeak.com"
tTransport = "websockets"
tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
tPort = 80 

class Sensors(threading.Thread):
		#serial port setting

	def __init__(self, pid, api, uport, filename):
		self.id = pid
		self.api = api
		self.port = uport
		self.filename = filename
		threading.Thread.__init__(self)

	def output(self):
		ser = serial.Serial(self.port, 9600)
		smoothing = 100

		#thingspeak setting
		channelID = self.id
		apiKey = self.api 
		topic = "channels/" + channelID + "/publish/" + apiKey

		with open(self.filename ,'w') as f:
			now = datetime.now()
			writer = csv.writer(f, lineterminator='\n')
			value = ser.readline()
			value = value.strip()
				#(hcho, mq135, co, humi, temp,)
			(hcho, mq135, co, humi, temp) = value.split(",")
			a = [now, value, hcho, mq135, co, humi, temp] 
			print(a)
			tPayload = "field1=" + hcho + "&field2=" + mq135 + "&field3=" + co + "&field4=" + humi + "&field5=" + temp 
			try:
				publish.single(topic, payload=tPayload, hostname=mqttHost,  transport=tTransport, port=tPort)
				print ( "success to write")
			except:
			 	print ("there was an error while publishing the data.")
try:
	while True:
		sensor1 = Sensors("210172", "VCZEBMUTCTMLAQUT", '/dev/cu.usbmodem14111', 'sensorlog1.csv')
		sensor2 = Sensors("210278", "FW1031YQE7P84KL5", '/dev/cu.usbmodem14141', 'sensorlog2.csv')
		sensor3 = Sensors("210283", "8ODO01FOLPIMHYY8", '/dev/cu.usbmodem14131', 'sensorlog3.csv')
		sensor1.start()
		sensor1.output()
		sensor2.start()
		sensor2.output()
		sensor3.start()
		sensor3.output()
except KeyboardInterrupt:
	print("finished")
	pass

