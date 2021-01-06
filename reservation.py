import sys
import requests
from ics import Calendar, Event
import arrow as arrow
from config import config_dict
import traceback

########
# Returns true if we have a reservation checking in today, false otherwise
########
def reservation_today():
    # Get the first event (we are assuming it's the soonest), check if we have a reservation checking in today
    tprint("Checking calendar for reservations today...")
    try:
        calendar_url = "https://colebergmann.com/sonos/test.ics"
        c = Calendar(requests.get(config_dict["cal_url"]).text)
        events = list(c.timeline)
        for i in range(0, len(events)):
            e = events[i] # first event in the list
            tprint("Event found for {} (starting {})".format(e.begin.format('YYYY-MM-DD'), e.begin.humanize()))
            if e.begin.format('YYYY-MM-DD') == arrow.utcnow().to('US/Pacific').format('YYYY-MM-DD'):
                tprint("We have a reservation starting today, returning True (from reservation_today)")
                return True
        # if we did not find a valid event, return False
        tprint("We DO NOT have a reservation starting today, returning False (from reservation_today)")
        return False
    except Exception as e:
        tprint("[Reservation] ERROR: An error occured while fetching the latest reservation. Assuming we don't have a reservation...")
        print(e)
        print(traceback.format_exc())
        return False

def tprint(s):
    print("\033[94m" + arrow.utcnow().to('US/Pacific').format('MM/DD/YYYY HH:mm') + " [Reservation]\033[0m " + s)

reservation_today()