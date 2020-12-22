# Sonos-Reservation-Door-Sensor
This project makes it possible to automatically play music on a Sonos system when an AirBnB/VRBO/whatever guest checks in and enters the house for the first time.

## Physical requirements:
- Sonos speakers
- N/O hardwired door sensor connected to ground and a GPIO pin on a Raspberry Pi
- A network connection on same subnet as Sonos speakers (wired or wireless)

## Configuration
See [`config.py`](config.py)
 to configure this project for your specific requirements.

 ## Arm / Disarm
 "Arming the door" refers to setting up the Sonos system and listening for the next door open event to trigger playing the music. The ics calendar at `cal_url` is checked at `arm_hour` every day to see if a guest is due to check in today. If a guest is due, the speakers queue the appropriate music and get it ready to play. This should be the time right before the next guest will have access to the property (ie: 14:59 for a 3pm checkin). `disarm_hour` is the time when the door will get disarmed if it has not been opened since arming. This is useful for disabling the automatic music after some time (maybe 9pm) so late arriving guests who want to sleep won't get annoyed.

 ## Dependencies
 - `SoCo` for controlling Sonos with Python
 - `arrow` for various date/time stuff
 - `RPi.GPIO` to interface with door sensor