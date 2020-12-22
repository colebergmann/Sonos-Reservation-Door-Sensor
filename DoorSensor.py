import time
from threading import Thread, Lock, Timer
from config import config_dict
import arrow as arrow
from Sonos import Sonos

def tprint(s):
        print("\033[94m" + arrow.utcnow().to('US/Pacific').format('MM/DD/YYYY HH:mm') + " [DoorSensor]\033[0m " + s)

on_pi_hardware = False
try:
    import RPi.GPIO as GPIO
    tprint("Running on Raspberry Pi")
    on_pi_hardware = True
except ImportError:
    tprint("Running on non-pi device, loop will not run")

class DoorSensor:

    # class variables
    door_open = False
    door_armed = False
    sensor_pin = config_dict["sensor_pin"]

    # init with whatever parameters 
    def __init__(self, sonos):
        self.sonos = sonos
        tprint("Constructed DoorSensor with pin " + str(self.sensor_pin))
        if on_pi_hardware:
            self.spawn_loop()

    def spawn_loop(self):
        tprint("Spawning a thread for watch_loop")
        t1 = Thread(target=self.watch_loop_sync)
        t1.start()

    # Loop to constantly monitor the door sensor so we can determine when it was triggered
    def watch_loop_sync(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        while True:
            sensor_state = GPIO.input(18)
            if self.door_open != sensor_state:
                self.door_open = sensor_state
                if self.door_open == True:
                    tprint("Door open")
                    if self.door_armed:
                        self.armed_door_opened()
                else:
                    tprint("Door closed")
                time.sleep(1)
            time.sleep(0.1)
    
    def armed_door_opened(self):
        tprint("Armed door was opened, playing music and disarming...")
        self.door_armed = False
        self.sonos.trigger()

    def arm_door(self):
        tprint("------ Door is now ARMED ------")
        self.door_armed = True
        self.sonos.prepare()
    
    def disarm_door(self):
        if self.door_armed:
            tprint("------ Door is DISARMED (without triggering) ------")
            self.door_armed = False
        else:
            tprint("Disarm called when door wasn't armed, ignoring")
    
    def is_door_open(self):
        return self.door_open

    def is_door_armed(self):
        return self.door_armed