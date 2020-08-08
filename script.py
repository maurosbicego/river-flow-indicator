import json
import os
import requests as r
from display import showmessage, lcd_init
import RPi.GPIO as GPIO

red = 11 #GPIO17
green = 13 # GPIO27
GPIO.setmode(GPIO.BOARD)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
state = 1
dirname = os.path.dirname(__file__)

with open(dirname + "config.json") as file:
    config = json.load(file)
station = str(config["station_id"])
threshold = config["threshold"]
endpoint = "https://api.existenz.ch/apiv1/hydro/latest?locations=" + station + "&parameters=flow,temperature&format=table&app=https%3A%2F%2Fgithub.com%2Fmaurosbicego%2Friver-flow-indicator"

try:
    data = r.get(endpoint).json()["payload"]
    flow = data[0]["val"]
    temperature = data[1]["val"]
    lcd_init()
    showmessage(str(round(flow)) + "m3/s - " + str(round(temperature, 1)) + "°C",1)
    if flow > threshold:
        showmessage(str(round(flow)) + "m3/s - Aare",1)
        showmessage("nicht befahrbar",2)
        GPIO.output(red, GPIO.HIGH)
        GPIO.output(green, GPIO.LOW)
    else:
        showmessage("Aare befahrbar",2)
        GPIO.output(red, GPIO.LOW)
        GPIO.output(green, GPIO.HIGH)
except:
    showmessage("Kein Internet",1)
    showmessage("Info per SMS",2)
