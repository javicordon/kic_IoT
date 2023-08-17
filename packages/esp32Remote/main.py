import os
import time
import ujson
import machine
import network
from umqtt.simple import MQTTClient

# InfraRed Libraries for Remote Control
from ir_tx import Player
from sys import platform
from machine import Pin
ir_cmd_msg = "" 


#Enter your wifi SSID and password below.
wifi_ssid = "JCOM_EPPM"
wifi_password = "746308592608"

#Enter your AWS IoT endpoint. You can find it in the Settings page of
#your AWS IoT Core console. 
#https://docs.aws.amazon.com/iot/latest/developerguide/iot-connect-devices.html 
aws_endpoint = b'a1dfeu6id51b8-ats.iot.us-west-1.amazonaws.com'

#If you followed the blog, these names are already set.
thing_name = "remotePrototype01"
client_id = "BlogClient"
private_key = "private.pem.key"
private_cert = "cert.pem.crt"

#Read the files used to authenticate to AWS IoT Core
with open(private_key, 'r') as f:
    key = f.read()
with open(private_cert, 'r') as f:
    cert = f.read()

# Configure Infrared Interface
if platform == 'esp32':
    pintx = Pin(32, Pin.OUT) # To be changed depending the board
ir = Player(pintx)

def sendIRcmd(cmdName = None):
    try:
        with open(cmdName, 'r') as f:
            cmdTX = ujson.load(f)
        ir.play(cmdTX)
    except:
        print('Command not found')
        ir_cmd_msg = "" 

#These are the topics we will subscribe to. We will publish updates to /update.
#We will subscribe to the /update/delta topic to look for changes in the device shadow.
topic_pub = "$aws/things/" + thing_name + "/shadow/update"
topic_sub = "$aws/things/" + thing_name + "/shadow/update/delta"
ssl_params = {"key":key, "cert":cert, "server_side":False}

#Define pins for LED and light sensor. In this example we are using a FeatherS2.
#The sensor and LED are built into the board, and no external connections are required.
led = machine.Pin(13, machine.Pin.OUT)
info = os.uname()

#Connect to the wireless network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to network...')
    wlan.connect(wifi_ssid, wifi_password)
    while not wlan.isconnected():
        pass

    print('Connection successful')
    print('Network config:', wlan.ifconfig())

def mqtt_connect(client=client_id, endpoint=aws_endpoint, sslp=ssl_params):
    mqtt = MQTTClient(client_id=client, server=endpoint, port=8883, keepalive=1200, ssl=True, ssl_params=sslp)
    print("Connecting to AWS IoT...")
    mqtt.connect()
    print("Done")
    return mqtt

def mqtt_publish(client, topic=topic_pub, message=''):
    print("Publishing message...")
    client.publish(topic, message)
    print(message)

def mqtt_subscribe(topic, msg):
    print("Message received...")
    message = ujson.loads(msg)
    print(topic, message)
    #if message['state']['led']:
    #    led_state(message)
    if message['state']['ir_cmd']:
        print('detected ir_cmd msg')
        ir_cmd(message)
    print("Done")

def led_state(message):
    #led.value(message['state']['led']['onboard'])
    print("Led dummy set")

def ir_cmd(message):
    cmd = message['state']['ir_cmd']['onboard']
    print(f'About to send command {cmd}')
    sendIRcmd(cmd)
    global ir_cmd_msg
    ir_cmd_msg = cmd
    print("Sent")

def displayStatus(sensor = 1):
    # Display temp/humidity and the remote last status
    # Sensor 0: Temperature in Celsius
    # Sensor 1: Humidity
    tNow = round(hdc.read_temperature(True),1)
    hNow = round(hdc.read_humidity(),1)
    display.fill(0)
    # Local Temperature
    if(sensor==1):
        display.text('Temp(C)', 3, 0, 1)
        display.text(str(tNow),15, 8, 1)
    elif(sensor==0):
        display.text('Humidit.', 0, 0, 1)
        display.text(str(hNow),15, 8, 1)    
    display.vline(61, 0, 16, 1)
    display.text('Rmt',69, 0, 1)
    rmtTempt = ir_cmd_msg[9:13]
    display.text(rmtTempt,65, 8, 1)
    display.show()
    return (tNow, hNow)

#We use our helper function to connect to AWS IoT Core.
#The callback function mqtt_subscribe is what will be called if we 
#get a new message on topic_sub.
try:
    print('start mqtt connect')
    mqtt = mqtt_connect()
    print('connect')
    mqtt.set_callback(mqtt_subscribe)
    print('subscribe mqtt')
    mqtt.subscribe(topic_sub)
    print('subscribe topic')
except Exception as e:
    print("Unable to connect to MQTT.")
    print(f"Error from connection {e}")

# Temperature Humidity and Display
from machine import Pin, I2C
import ssd1306
import hdc1080
i2c = I2C(1, sda=Pin(26), scl=Pin(27))
hdc = hdc1080.HDC1080(i2c=i2c)
display = ssd1306.SSD1306_I2C(96, 16, i2c)
tempHumid = 1
while True:
#Check for messages.
    try:
        mqtt.check_msg()
    except:
        print("Unable to check for messages.")

    #Once checked a message, update display status
    (tNow, hNow) = displayStatus(tempHumid)
    tempHumid = 0 if tempHumid == 1 else 1

    mesg = ujson.dumps({
        "state":{
            "reported": {
                "device": {
                    "client": client_id,
                    "uptime": time.ticks_ms(),
                    "hardware": info[0],
                    "firmware": info[2]
                },
                "sensors": {
                    "light": 0,
                    "humidity": hNow,
                    "temperature": tNow,
                },
                "led": {
                    "onboard": led.value()
                },
                "ir_cmd": {
                    "onboard": ir_cmd_msg
                }
            }
        }
    })

#Using the message above, the device shadow is updated.
    #try:
    mqtt_publish(client=mqtt, message=mesg)
    #except Exception as e:
    #   print("Unable to publish message.")
    #    print(e)

#Wait for 10 seconds before checking for messages and publishing a new update.
    print("Sleep for 10 seconds")
    time.sleep(10)