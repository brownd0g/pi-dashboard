from flask import Flask, render_template, make_response
import random
from time import time
import json
#import RPi.GPIO as GPIO

app = Flask(__name__)

@app.route('/')
def index():
    penis = "penis"
    return render_template('index1.html', penis=penis)

@app.route('/on')
def on():
    # open door
    print("ON")
    return render_template('index.html')

@app.route('/off')
def off():
    print("OFF")
    return render_template('index.html')

@app.route('/button')
def button():
    return render_template('button.html')

@app.route('/widget')
def widget():
    return render_template('widget.html')

@app.route('/data')
def data():
    indoorTemp = random.random() * 100
    outdoorTemp = random.random() * 50
    data = [time() * 1000, indoorTemp, outdoorTemp]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


app.run(host='0.0.0.0', port='5000', debug=True)