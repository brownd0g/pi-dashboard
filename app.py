from flask import Flask, render_template, make_response, jsonify
import random
from time import time
import json
#import RPi.GPIO as GPIO
#from w1thermsensor import W1ThermSensor
import requests

app = Flask(__name__)

# pi sensors
#sensor = W1ThermSensor()
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(21, GPIO.OUT)

# esp8266 ips
#fridgeEsp = 'http://...' put fridge esp8266 ip here
doorEsp = "http://10.0.0.117/" #put door esp8266 ip here
outdoorRearEsp = "http://10.0.0.56/"
outdoorTempURL = outdoorRearEsp + "temperature"
outdoorLocation = "Outside"
PARAMS = {'tempOneUrl':outdoorLocation}


@app.route('/')
def index():
    penis = "penis"
    return render_template('index1.html', penis=penis)

@app.route('/on')
def on():
    return render_template('index.html')

@app.route('/off')
def off():
    return render_template('index.html')

@app.route('/doorbell')
def doorbell():
    url = doorEsp + "doorbell"
    db = requests.get(url=url, params=PARAMS)
    db = db.content
    dbJson = {"Door": db}
    print("URL----------------------------------------------:")
    print(url)
    print("db----------------------------------------------:")
    print(db)
    response = make_response(jsonify(dbJson))
    response.content_type = 'application/json'
    return response

@app.route('/data')
def data():
    pass

    # fridgeTemp = sensor.get_temperature()
    # fridgeTemp = 1
    # indoorTemp = random.random() * 100
    # outdoorTemp = requests.get(url=outdoorTempURL, params=PARAMS)
    # outdoorTemp = float(outdoorTemp.content)

    # data = [time() * 1000, fridgeTemp, indoorTemp, outdoorTemp]
    # if fridgeTemp > 22:
    #     print('Relay On')
    #     GPIO.output(21, GPIO.HIGH)
    # else:
    #     GPIO.output(21, GPIO.LOW)
    # response = make_response(json.dumps(data))
    # response.content_type = 'application/json'
    # return response

######################################


app.run(host='0.0.0.0', port='5000', debug=True)