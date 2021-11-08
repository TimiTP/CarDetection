import paho.mqtt.client as mqtt
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):

    print("Connected with result code "+str(rc))
    
def speedlimit(i):
    
    switcher = {
        30: '30',
        40: '40',
        50: '50',
        60: '60',
        80: '80',
        100: '100',
        120: '120'
    }
    return switcher.get(i,'invalid')
        

client = mqtt.Client()
client.on_connect = on_connect

client.connect("broker.hivemq.com", 1883, 60)

client.loop_start()
time.sleep(1)
while True:
    
    choice = input("Valitse nopeus: 30,40,50,60,80,100,120\n")
    choice = int(choice)
    #choice = int(input(...))

    client.publish("testi",speedlimit(choice))
    time.sleep(2)

client.loop_stop()
client.disconnect()