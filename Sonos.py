import time
from threading import Thread, Lock, Timer
from config import config_dict
import arrow
import soco
import traceback

class Sonos:
 
    # init with whatever parameters 
    def __init__(self):
        tprint("Sonos object created. Doing nothing until called")
        self.primary_speaker = None

    # prepare sonos system
    # search for speakers, group them, set volume, set track, pause
    def prepare(self):
        tprint("Requested to prepare system")
        tprint("Searching for speakers...")
        self.primary_speaker = soco.discovery.any_soco()

        # Perform some actions on the group
        try:
            if self.primary_speaker:
                tprint("Found speakers, using " + self.primary_speaker.player_name + " as primary speaker")
                self.primary_speaker.group.coordinator.partymode()
                tprint("Using " + self.primary_speaker.player_name + " as primary speakers and starting partymode")
                self.primary_speaker.group.coordinator.partymode()
                tprint("Queueing music and pausing")
                #self.primary_speaker.group.coordinator.volume = config_dict["sonos_volume"]
                # set volume of all speakers in group
                for speaker in self.primary_speaker.group.members:
                    tprint(" -> Setting volume on " + speaker.player_name)
                    speaker.volume = config_dict["sonos_volume"]
                self.primary_speaker.group.coordinator.play_uri(config_dict["sonos_track_url"])
                self.primary_speaker.group.coordinator.pause()
            else:
                raise Exception("Speaker group was null, can't prepare with no speakers")
        except Exception as e:
            print(e)
            tprint("ERROR: An error occured while preparing the Sonos speakers. Unable to proceed.")
            print(traceback.format_exc())


    # start playback
    # retain the previous sonos object and immediately start playing music
    # this should happen ASAP so the users won't hear a delay between opening the door and starting the music
    def trigger(self):
        tprint("Request to trigger playback")
        try:
            if self.primary_speaker:
                self.primary_speaker.group.coordinator.play()
                tprint("Sent play command to Sonos")
            else:
                raise Exception("Speaker group was null, can't start playback")
        except Exception as e:
            print(e)
            tprint("An error occured while triggering playback of Sonos")


def tprint(s):
        print("\033[94m" + arrow.utcnow().to('US/Pacific').format('MM/DD/YYYY HH:mm') + " [Sonos]\033[0m " + s)