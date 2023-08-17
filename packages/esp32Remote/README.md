# ESP32 Remote Controller

Hi! In this repo you will find our code to make the ESP32 work as a **Remote Controller**. It also connects to AWS MQTT IoT Core, where it expects deltas that come from Alexa, when a new  command is sent. Once it detects the new command, the ESP32 will go and get the file command (previously recorded), and send the Infra Red (IR) command.

# Files

StackEdit stores your files in your browser, which means all your files are automatically saved locally and are accessible **offline!**

## main
main.py
It contains all the program for connecting the ESP32 to AWS.
Functions that will detect the deltas of the JSON.
Fetch the local command and schedule to send it in IR.
Get temperature and humidity from local sensor.
Display temperature, humidity and latest IR command sent on LCD Display.

## recordCommands

Is a customizable independent program.
It is used to record the IR commands from a remote control.
After, they can be retrieved for reproducing recorded remote control commands.

#### Last Review

August 17th 2023