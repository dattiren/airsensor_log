from __future__ import print_function
import csv
import serial
from time import sleep
from datetime import datetime
import paho.mqtt.publish as publish
import psutil

#serial port setting
ser = serial.Serial('/dev/cu.usbmodem14241', 9600)
smoothing = 100

#thingspeak setting
channelID = "206998"
apiKey = "LCDNR6WDV5MIFUUA"
useSSLWebsockets = True
mqttHost = "mqtt.thingspeak.com"
import ssl
tTransport = "websockets"
tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
tPort = 80 
topic = "channels/" + channelID + "/publish/" + apiKey

with open('airSensorLog.csv','w') as f:
	try:
	  while True:
		time = datetime.now()
		writer = csv.writer(f, lineterminator='\n')
		value = ser.readline()
		value = value.strip()
		#(hcho, mq135, humi, temp,)
		(humi, temp) = value.split(",")
		#curl https://api.thingspeak.com/update/ -X POST -d field1=value  -H 'X-THINGSPEAKAPIKEY:LCDNR6WDV5MIFUUA'
		a = [time, value, humi,temp] 
		##writer.writerow(a)
		print(a)
		#cpuPercent = psutil.cpu_percent(interval=20)
		#ramPercent = psutil.virtual_memory().percent
		#print (" CPU =",cpuPercent,"   RAM =",ramPercent)
		#tPayload = "field1=" + value
		tPayload = "field3=" + humi  + "&field4=" + temp
		try:
			publish.single(topic, payload=tPayload, hostname=mqttHost,  transport=tTransport, port=tPort)
			print ( "success to write")
		except (KeyboardInterrupt):
			break
		except:
			print ("There was an error while publishing the data.")
	except KeyboardInterrupt:
		f.close()
		print("csv wrote")
		pass
