# clear console before starting
for i in range(0,40):
    print("\n")

from config import config_dict
from DoorSensor import DoorSensor
from DoorScheduler import DoorScheduler
import sys, os
import arrow
from Sonos import Sonos

def tprint(s):
        print("\033[94m" + arrow.utcnow().to('US/Pacific').format('MM/DD/YYYY HH:mm') + " [Runner]\033[0m " + s)

def bool_str(b):
    if b:
        return "True"
    return "False"
tprint("Starting....")

sonos = Sonos()
door_sensor = DoorSensor(sonos)
door_scheduler = DoorScheduler(door_sensor)

tprint("Initialization done")

while True:
    cmd = input("-> (config/status/exit/arm/disarm) ")
    if cmd == "status":
        print("\tDoor open: " + bool_str(door_sensor.is_door_open()))
        print("\tDoor armed: " + bool_str(door_sensor.is_door_armed()))
    elif cmd == "config":
        for c in config_dict:
            print("\t["+c+"] " + str(config_dict[c]))
    elif cmd == "exit" or cmd == "q":
        tprint("adios!")
        os._exit(9)
    elif cmd == "arm":
        door_sensor.arm_door()
    elif cmd == "disarm":
        door_sensor.disarm_door()
    elif cmd == "clear":
        for i in range(0, 40):
            print("")
    else:
        print("Unknown command: <" + cmd + ">")