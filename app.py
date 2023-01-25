
from flask import Flask, render_template, make_response, jsonify, request

import json
import requests
from requests.adapters import HTTPAdapter, Retry

import create_response as ESP

# esp8266 ips
ip_door = "http://10.0.0.117/"
ip_roof = "http://10.0.0.118/"
ip_tv = "http://10.0.0.119/"
ip_aircon = "http://10.0.0.126/"

# esp objects
esp_door = ESP.Esp("esp_door", ip_door, None, "switch")
esp_roof = ESP.Esp("esp_roof", ip_roof, None, "state")
esp_tv = ESP.Esp("esp_tv", ip_tv, None, "switch")
esp_aircon = ESP.Esp("esp_aircon", ip_aircon, None, "switch")

outdoorLocation = "test"
PARAMS = {'test': outdoorLocation}

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

s = requests.Session()
retries = Retry(total=0, backoff_factor=0.0, status_forcelist=[500, 502, 503, 504])


def get_states():
    tout = 0.1

    s.mount(esp_door.ip, HTTPAdapter(max_retries=retries))
    s.mount(esp_roof.ip, HTTPAdapter(max_retries=retries))
    s.mount(esp_tv.ip, HTTPAdapter(max_retries=retries))
    s.mount(esp_aircon.ip, HTTPAdapter(max_retries=retries))

    try:
        door_raw = s.get(url=esp_door.path, timeout=tout)
        door_raw = json.loads(door_raw.content.decode())
        esp_door.status = "online"
        esp_door.data = door_raw["esp_door"]["data"]

    except requests.exceptions.RequestException as e:
        esp_door.status = "offline"
        esp_door.data = "none"

    try:
        roof_raw = s.get(url=esp_roof.path, timeout=tout)
        roof_raw = json.loads(roof_raw.content.decode())
        esp_roof.status = "online"
        esp_roof.data = roof_raw["esp_roof"]["data"]

    except requests.exceptions.RequestException as e:
        esp_roof.status = "offline"
        esp_roof.data = "none"

    try:
        tv_raw = s.get(url=esp_tv.path, timeout=tout)
        tv_raw = json.loads(tv_raw.content.decode())
        esp_tv.status = "online"
        esp_tv.data = tv_raw["esp_roof"]["data"]

    except requests.exceptions.RequestException as e:
        esp_tv.status = "offline"
        esp_tv.data = "none"

    merged_dict = esp_door.get_json()
    merged_dict.update(esp_roof.get_json())
    merged_dict.update(esp_tv.get_json())

    all_states = json.dumps(merged_dict, indent=2)
    return all_states


@app.route('/api/state')
def index():

    response = make_response(get_states())
    response.content_type = 'application/json'
    print(get_states())
    return response

@app.route('/api/aircon', methods=['POST', 'GET'])
def set_aircon():
    url = esp_aircon.ip + "aircon"
    action = request.args
    action = action.to_dict()
    data_raw = requests.post(url=url, data=action,)
    data = data_raw.content.decode()

    json_object = json.loads(data)
    json_formatted_str = json.dumps(json_object, indent=2)
    response = make_response(json_formatted_str)

    response.content_type = 'application/json'
    print(json_formatted_str)
    return response


@app.route('/api/teams', methods=['POST', 'GET'])
def set_call_state():
    url = esp_aircon.ip + "teams"
    action = request.args
    action = action.to_dict()
    print(action)
    data_raw = requests.post(url=url, data=action,)
    data = data_raw.content.decode()

    json_object = json.loads(data)
    json_formatted_str = json.dumps(json_object, indent=2)
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

