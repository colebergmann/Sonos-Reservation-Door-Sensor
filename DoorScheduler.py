import time
from threading import Thread, Lock, Timer
from config import config_dict
import arrow as arrow

class DoorScheduler:

    def check_time(self):
        Timer(60.0, self.check_time).start()
        current_time = arrow.utcnow().to('US/Pacific').format('HH:mm')
        if current_time == self.arm_time:
            self.arm_check
        elif current_time == self.disarm_time:
            self.disarm_check()

    # init with whatever parameters 
    def __init__(self):
        self.arm_time = config_dict["arm_hour"]
        self.disarm_time = config_dict["disarm_hour"]
        tprint("Constructed scheduler with arm_hour=" + str(self.arm_time) + ", disarm_hour=" + str(self.disarm_time))
        self.check_time()

    # Check if we have a reservation today
    # If we do, set the door sensor to ARMED
    def arm_check(self):
        tprint("It's " + self.arm_time + ", running arm check")

    # Call disarm in door sensor
    def disarm_check(self):
        tprint("It's " + self.disarm_time + ", running disarm check")


def tprint(s):
        print("[DoorScheduler] " + s)

DoorScheduler()