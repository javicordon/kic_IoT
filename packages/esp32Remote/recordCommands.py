from ir_tx import Player
from acquire import test
from sys import platform
from machine import Pin
from time import sleep
import ujson


# TX
if platform == 'esp32':
    pintx = Pin(32, Pin.OUT)
ir = Player(pintx)

lst = test()
with open('burst.py', 'w') as f:
    ujson.dump(lst, f)

with open('burst.py', 'r') as f:
cmdTX = ujson.load(f)

ir.play(cmdTX)

# Commands that have multiple meassures to record

cmdNames = ['coldAuto','coldHigh']
cmdTemp = 16.0
cmdTempEnd   = 30.0
delta   = 0.5

for cmdName in cmdNames:
while cmdTemp!=(cmdTempEnd+delta):
fileName = f"{cmdName}_{cmdTemp}.py"
print(f"Record {cmdName} at {cmdTemp}")
cmd = test()

cmdTemp = cmdTemp+delta
print(f"Recording file {fileName}")
with open(fileName, 'w') as f:
ujson.dump(cmd, f)
print("Done Recording")
sleep(0.3)


# Specific commands
cmds = ['stop'] # List of command names to record
for cmd in cmds:
print(f"Record {cmd}")
fileName = f"{cmd}.py"
cmd = test()
print(f"Recording file {fileName}")
with open(fileName, 'w') as f:
ujson.dump(cmd, f)
print("Done Recording")
sleep(0.3)