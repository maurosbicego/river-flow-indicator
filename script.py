import json
import requests as r
state = 1
with open("config.json") as file:
    config = json.load(file)
station = str(config["station_id"])
threshold = config["threshold"]
endpoint = "https://api.existenz.ch/apiv1/hydro/latest?locations=" + station + "&parameters=flow&format=table&app=https%3A%2F%2Fgithub.com%2Fmaurosbicego%2Friver-flow-indicator"

flow = r.get(endpoint).json()["payload"][0]["val"]
if flow > threshold:
    state = 0
else:
    state = 1
