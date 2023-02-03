
from flask import Flask, render_template, make_response, jsonify, request

import json
import requests
from requests.adapters import HTTPAdapter, Retry
from server_state import server_state
import atexit

from apscheduler.schedulers.background import BackgroundScheduler


import create_response as ESP

# esp8266 ips and objects
ip_door = "http://10.0.0.117/"
esp_door = ESP.Esp("esp_door", ip_door)

ip_roof = "http://10.0.0.118/"
esp_roof = ESP.Esp("esp_roof", ip_roof)

ip_aircon = "http://10.0.0.126/"
esp_aircon = ESP.Esp("esp_aircon", ip_aircon)
esp_aircon.ip_paths["post_aircon"] = ip_aircon + "aircon"
esp_aircon.ip_paths["post_teams"] = ip_aircon + "teams"
esp_aircon.ip_paths["get_state"] = ip_aircon + "state"


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

s = requests.Session()
retries = Retry(total=0, backoff_factor=0.0, status_forcelist=[500, 502, 503, 504])


def get_states():
    tout = 0.1

    s.mount(esp_door.ip, HTTPAdapter(max_retries=retries))
    s.mount(esp_roof.ip, HTTPAdapter(max_retries=retries))
    s.mount(esp_aircon.ip, HTTPAdapter(max_retries=retries))

    try:
        door_raw = s.get(url=esp_door.ip_paths["get_state"], timeout=tout)
        door_raw = json.loads(door_raw.content.decode())
        esp_door.status = "online"
        esp_door.data = door_raw["esp_door"]["data"]

    except requests.exceptions.RequestException as e:
        esp_door.status = "offline"
        esp_door.data = {}
    except:

        esp_door.status = "offline"
        esp_door.data = {}

    try:
        roof_raw = s.get(url=esp_roof.ip_paths["get_state"], timeout=tout)
        roof_raw = json.loads(roof_raw.content.decode())
        esp_roof.status = "online"
        esp_roof.data = roof_raw["esp_roof"]["data"]

    except requests.exceptions.RequestException as e:
        esp_roof.status = "offline"
        esp_roof.data = {}
    except:
        esp_roof.status = "offline"
        esp_roof.data = {}

    try:
        aircon_raw = s.get(url=esp_aircon.ip_paths["get_state"], timeout=tout)
        aircon_raw = json.loads(aircon_raw.content.decode())
        esp_aircon.status = "online"
        esp_aircon.data = aircon_raw["esp_aircon"]["data"]

    except requests.exceptions.RequestException as e:
        esp_aircon.status = "offline"
        esp_aircon.data = {}
    except:
        esp_aircon.status = "offline"
        esp_aircon.data = {}


scheduler = BackgroundScheduler()
scheduler.add_job(func=get_states, trigger="interval", seconds=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.route('/api/state', methods=['POST', 'GET'])
def index():
    response = ESP.create_json_response([esp_door, esp_roof, esp_aircon])
    response.content_type = 'application/json'
    return response

@app.route('/api/aircon', methods=['POST', 'GET'])
def set_aircon():
    url = esp_aircon["ip_paths"]["post_aircon"]
    action = request.args.to_dict()
    #action = action.to_dict()
    data_raw = requests.post(url=url, data=action)
    data = data_raw.content.decode()
    response_dict = json.loads(data)

    if "data" in response_dict:
        esp_aircon.data = response_dict["data"]
    else:
        esp_aircon.data = {}

    json_formatted_str = json.dumps(esp_aircon.get_json(), indent=2)
    response = make_response(json_formatted_str)

    response.content_type = 'application/json'
    return response


@app.route('/api/teams', methods=['POST', 'GET'])
def set_call_state():
    url = esp_aircon["ip_paths"]["post_teams"]
    action = request.args.to_dict()
    #action = action.to_dict()
    print(action)
    data_raw = requests.post(url=url, data=action,)
    data = data_raw.content.decode()
    response_dict = json.loads(data)

    if "data" in response_dict:
        esp_aircon.data = response_dict["data"]
    else:
        esp_aircon.data = {}

    json_formatted_str = json.dumps(esp_aircon.get_json(), indent=2)
    response = make_response(json_formatted_str)

    response.content_type = 'application/json'
    return response


# @app.route('/api/roof/lights')
# def login():
#     url = roof_esp + "switch"
#     action = request.args
#     action = action.to_dict()
#     data_raw = requests.post(url=url, data=action,)
#     data = data_raw.content.decode()
#
#     json_object = json.loads(data)
#     json_formatted_str = json.dumps(json_object, indent=2)
#     response = make_response(json_formatted_str)
#
#     response.content_type = 'application/json'
#     return response
#
#
# @app.route('/api/shelf/lights')
# def rgb():
#     url = roof_esp + "switch"
#     action = request.args
#     action = action.to_dict()
#     col = list(action.keys())[0]
#     val = list(action.values())[0]
#
#     if col == "rgb":
#         colourDict["red"] = val
#         colourDict["green"] = val
#         colourDict["blue"] = val
#     else:
#         colourDict[col] = val
#     print(action)
#     #print(colourDict)
#
#     requests.post(url=url, data=action)
#     txt = json.dumps(colourDict, indent=2)
#     response = make_response(txt)
#     response.content_type = 'application/json'
#     return response
#
#
# @app.route('/api/shelf/state')
# def rgbState():
#     txt = json.dumps(colourDict, indent=2)
#     response = make_response(txt)
#     response.content_type = 'application/json'
#     return response
#
#
# @app.route('/api/tv/lights')
# def tv_light():
#
#     tv_url = tv_esp + "switch"
#     print(tv_url)
#     action = request.args
#     action = action.to_dict()
#     #print(action)
#
#     data_raw = requests.post(url=tv_url, data=action, )
#     print(data_raw)
#     data = data_raw.content.decode()
#     print(data)
#     json_object = json.loads(data)
#     print(json_object)
#
#     json_formatted_str = json.dumps(json_object, indent=2)
#     print(json_formatted_str)
#     response = make_response(json_formatted_str)
#
#     response.content_type = 'application/json'
#     return response


app.run(host='0.0.0.0', port='5000', debug=True)

