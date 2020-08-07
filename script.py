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
endpoint = "https://api.existenz.ch/apiv1/hydro/latest?locations=" + station + "&parameters=flow,temperature&format=table&app=https%3A%2F%2Fgithub.com%2Fmaurosbicego%2Friver-flow-indicator"

data = r.get(endpoint).json()["payload"]
flow = data[0]["val"]
temperature = [1]["val"]
lcd_init()
showmessage(str(flow) + "m³/s, " + str(temperature) + " °C",1)
if flow > threshold:
    showmessage("Nicht befahrbar",2)
    GPIO.output(red, GPIO.HIGH)
    GPIO.output(green, GPIO.LOW)
else:
    showmessage("Aare befahrbar",2)
    GPIO.output(red, GPIO.LOW)
    GPIO.output(green, GPIO.HIGH)
