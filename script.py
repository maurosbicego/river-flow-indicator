import json
import requests as r
from display import showmessage, lcd_init
import RPi.GPIO as GPIO

red = 11 #GPIO17
green = 13 # GPIO27
GPIO.setmode(GPIO.BOARD)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
state = 1
with open("config.json") as file:
    config = json.load(file)
station = str(config["station_id"])
threshold = config["threshold"]
endpoint = "https://api.existenz.ch/apiv1/hydro/latest?locations=" + station + "&parameters=flow&format=table&app=https%3A%2F%2Fgithub.com%2Fmaurosbicego%2Friver-flow-indicator"

flow = r.get(endpoint).json()["payload"][0]["val"]
lcd_init()
showmessage(str(flow),1)
if flow > threshold:
    showmessage("Aare nicht befahrbar",2)
    GPIO.output(rot, GPIO.HIGH)
    GPIO.output(green, GPIO.LOW)
else:
    showmessage("Aare befahrbar",2)
    GPIO.output(rot, GPIO.LOW)
    GPIO.output(green, GPIO.HIGH)
