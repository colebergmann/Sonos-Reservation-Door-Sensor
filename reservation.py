import sys
import requests
from ics import Calendar, Event
import arrow as arrow
from config import config_dict

########
# Returns true if we have a reservation checking in today, false otherwise
########
def reservation_today():
    # Get the first event (we are assuming it's the soonest), check if we have a reservation checking in today
    tprint("Checking calendar for reservations today...")
    try:
        calendar_url = "https://colebergmann.com/sonos/test.ics"
        c = Calendar(requests.get(config_dict["cal_url"]).text)
        e = list(c.timeline)[0] # first event in the list
        tprint("Event found for {} (starting {})".format(e.begin.format('YYYY-MM-DD'), e.begin.humanize()))
        if e.begin.format('YYYY-MM-DD') == arrow.utcnow().format('YYYY-MM-DD'):
            tprint("We have a reservation starting today, returning True (from reservation_today)")
            return True
        else:
            tprint("We DO NOT have a reservation starting today, returning False (from reservation_today)")
            return False
    except Exception as e:
        tprint("[Reservation] ERROR: An error occured while fetching the latest reservation. Assuming we don't have a reservation...")
        print(e)
        return False

def tprint(s):
    print("[Reservation] " + s)