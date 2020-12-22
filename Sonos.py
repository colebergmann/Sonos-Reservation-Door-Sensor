import time
from threading import Thread, Lock, Timer
from config import config_dict
import arrow
import soco

class Sonos:
 
    # init with whatever parameters 
    def __init__(self):
        tprint("Sonos object created. Doing nothing until called")
        self.group = None

    # prepare sonos system
    # search for speakers, group them, set volume, set track, pause
    def prepare(self):
        tprint("Requested to prepare system")
        tprint("Searching for speakers...")
        for zone in soco.discover():
            tprint("\tDiscovered " + zone.player_name)
            if zone.player_name == "Garage":
                self.group = zone

        # Perform some actions on the group
        try:
            if self.group:
                self.group.volume = config_dict["sonos_volume"]
                self.group.play_uri(config_dict["sonos_track_url"])
                self.group.pause()
            else:
                raise Exception("Speaker group was null, can't control if we didn't find the group we wanted")
        except Exception as e:
            print(e)
            tprint("ERROR: An error occured while preparing the Sonos speakers. Unable to proceed.")


    # start playback
    # retain the previous sonos object and immediately start playing music
    # this should happen ASAP so the users won't hear a delay between opening the door and starting the music
    def trigger(self):
        tprint("Request to trigger playback")
        try:
            self.group.play()
            tprint("Sent play command to Sonos")
        except Exception as e:
            print(e)
            tprint("An error occured while triggering playback of Sonos")


def tprint(s):
        print("\033[94m" + arrow.utcnow().to('US/Pacific').format('MM/DD/YYYY HH:mm') + " [Sonos]\033[0m " + s)
