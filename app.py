from flask import Flask, make_response, request

import json
import requests
from requests.adapters import HTTPAdapter, Retry
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
import create_response as ESP
from esp_definitions import ESP_TV

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

s = requests.Session()
retries = Retry(total=1, backoff_factor=0.0, status_forcelist=[500, 502, 503, 504])
s.mount(ESP_TV.ip, HTTPAdapter(max_retries=retries))

def get_states():
    try:
        requests.post(url=ESP_TV.ip_paths["post_teams"], data=ESP_TV.data)
        print("ESP FROM GET STATES", ESP_TV.data)
        if ESP_TV.isSet:
            response_raw = requests.post(url=ESP_TV.ip_paths["post_aircon"], data=ESP_TV.data["aircon"])
            print("IF ESPISSET")
        else:
            print("IF NOT ESPISSET")
            response_raw = requests.get(url=ESP_TV.ip_paths["get_state"])
            tv_raw = response_raw.content.decode()
            tv_json = json.loads(tv_raw)
            ESP_TV.data["aircon"] = tv_json["ESP_TV"]["data"]["aircon"]
            ESP_TV.isSet = True
        ESP_TV.status = "online" if response_raw.status_code == 200 else "offline"

    except requests.exceptions.RequestException as e:
        print("FAILED REQUEST")
        ESP_TV.status = "offline"
    except:
        print("FAILED FOR SOME OTHER FUCKING REASON CUNT")
        ESP_TV.status = "offline"


@app.route('/api/state', methods=['POST', 'GET'])
def index():
    response = ESP.create_json_response([ESP_TV])
    response.content_type = 'application/json'
    return response


@app.route('/api/aircon/set_state', methods=['POST', 'GET'])
def set_aircon():
    action = request.args.to_dict()

    if "data" in action:
        ESP_TV.data = action["data"]

    json_formatted_str = json.dumps(ESP_TV.get_json(), indent=2)
    response = make_response(json_formatted_str)

    response.content_type = 'application/json'
    return response


@app.route('/api/teams', methods=['POST', 'GET'])
def set_call_state():
    action = request.args.to_dict()

    if "status" in action:
        ESP_TV.data["teams_status"] = action["status"]

    resp = ESP_TV.get_json()
    json_formatted_str = json.dumps(resp["esp_aircon"], indent=2)
    response = make_response(json_formatted_str)
    response.content_type = 'application/json'

    return response


scheduler = BackgroundScheduler()
scheduler.add_job(func=get_states, trigger="interval", seconds=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
