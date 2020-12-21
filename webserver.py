from flask import render_template, Flask, request, redirect, session
from threading import Thread
from config import config_dict
from DoorSensor import DoorSensor

app = Flask(__name__)

global door_sensor

@app.route('/')
@app.route('/index')
def home():
    log_events = []
    with open("events.log") as f:
        log_events = f.readlines()
    # strip web log lines
    for item in list(log_events):
        if "HTTP" in item:
            log_events.remove(item)
    log_events.reverse()

    status = ""
    btn_name = "ARM DOOR"
    btn_url = "/arm"
    btn_color = "danger"
    if door_sensor.is_door_open():
        status = "OPENED, "
    else:
        status = "CLOSED, "
    
    if door_sensor.is_door_armed():
        status += "ARMED"
        btn_name = "DISARM DOOR"
        btn_url = "/disarm"
        btn_color = "success"
    else:
        status += "NOT ARMED"
    return render_template('main.html', title='Home', data=config_dict, events=log_events, status_msg=status, btn_name=btn_name, btn_url=btn_url, btn_color=btn_color)

@app.route("/arm")
def armdoor():
    door_sensor.arm_door()
    return redirect("/", code=303)

@app.route("/disarm")
def unarmdoor():
    door_sensor.disarm_door()
    return redirect("/", code=303)

# start the webserver
if __name__ == "__main__":
    door_sensor = DoorSensor()
    app.debug = True
    app.secret_key = 'KMergmkerg8ergmklzmagnja8rg8rgnamgr'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(use_reloader=False, host='0.0.0.0')