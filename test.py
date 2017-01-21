from __future__ import print_function
import csv
import serial
from time import sleep
import time 
from datetime import datetime
import paho.mqtt.publish as publish
import psutil
import ssl
#import threading
import io

useSSLWebsockets = True
mqttHost = "mqtt.thingspeak.com"
tTransport = "websockets"
tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
tPort = 80 
devices = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2']
ser1 = serial.Serial(devices[0], 9600, timeout=2)
ser2 = serial.Serial(devices[1], 9600, timeout=2)
ser3 = serial.Serial(devices[2], 9600, timeout=2)
class Sensors():
		#serial port setting

	def __init__(self, pid, api, filename, ser):
		self.id = pid
		self.api = api
		self.filename = filename
		self.ser = ser
		#threading.Thread.__init__(self)

	def output(self):
		sio = io.TextIOWrapper(io.BufferedRWPair(self.ser,self.ser), errors='ignore')
		#thingspeak setting
		channelID = self.id
		apiKey = self.api 
		topic = "channels/" + channelID + "/publish/" + apiKey

		with open(self.filename ,'a') as f:
			now = datetime.now()
			writer = csv.writer(f, lineterminator='\n')

			value = sio.readline()
			print(self.id + "," +value)
			list = value.split(",")
			if(len(list) == 4):
				(hcho, mq135, humi, temp) = value.split(",")
				a = [now, hcho, mq135, humi, temp] 
				writer.writerow(a)
				tPayload = "field1=" + hcho + "&field2=" + mq135 + "&field4=" + humi + "&field5=" + temp 
				try:
					publish.single(topic, payload=tPayload, hostname=mqttHost,  transport=tTransport, port=tPort)
					print ( "success to write")
				except:
			 		print ("there was an error while publishing the data.")
try:
	sensor1 = Sensors("210172", "vczebmutctmlaqut",  'sensorlog1.csv' , ser1) 
	sensor2 = Sensors("210278", "fw1031yqe7p84kl5",  'sensorlog2.csv' , ser2) 
	sensor3 = Sensors("210283", "8odo01folpimhyy8",  'sensorlog3.csv' , ser3) 

	while True:
		sensor1.output()
		ser1.open()
		time.sleep(1)
		sensor2.output()
		ser2.open()
		time.sleep(1)
		sensor3.output()
		ser3.open()
		time.sleep(1)

except KeyboardInterrupt:
	print("finished")
	pass
