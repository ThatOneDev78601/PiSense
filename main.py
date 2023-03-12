#Variables
from sense_hat import SenseHat
from gpiozero import CPUTemperature
from datetime import datetime
from ISStreamer.Streamer import Streamer
bkey = "2fb27f6a-84c8-44c5-9c6e-3d61da431579" #Made key viewable in file directory because I doubt anyone will view it. However in a proper project should be in as an environmental variable
key = "ist_1cvQJOd60hKx0j_IViCDjwXp-rdHl4MB"
import sys
import time
import math

sense = SenseHat()
logger = Streamer(bucket_name="RPI SENSE HAT DATA", bucket_key=bkey, access_key=key)
flashon = False

#Functions
def flashlight():
    global flashon
    if flashon == False:
        flashon = True
        sense.clear(255,255,255)
    else:
        flashon = False
        sense.clear(0,0,0)


def gethumidity():
    flashon = False
    humidity = sense.get_humidity()
    logger.log("Humidity:", humidity)
    return math.floor(humidity)

def gettemp():
    flashon = False
    temp = sense.get_temperature_from_humidity()
    logger.log("Temperature:", temp)
    return math.floor(temp)
def getpressure():
    flashon = False
    ps = sense.get_pressure()
    logger.log("Pressure:", ps)
    return math.floor(ps)

def handle_events(movement):

    if movement == "up":
        sense.clear()
        sense.show_message(f"Temp: {gettemp()}")
        pass
    elif movement == "down":
        sense.clear()
        flashlight()
        pass
    elif movement == "right":
        sense.clear()
        sense.show_message(f"Air Pressure: {getpressure()}")
        pass
    elif movement == "left":
        sense.clear()
        sense.show_message(f"Air Humidity: {gethumidity()}")
        pass
    elif movement == "enter":
        sense.clear()
        time = datetime.now()
        hour = time.hour
        minute = time.minute
        if hour >12:
            hour -= 12
        if minute <= 9:
            minute = f"0{minute}"

        sense.show_message(f"{hour}:{minute}")
        pass


sense.clear()
while True:

    for event in sense.stick.get_events():

        if event.direction == "up" and event.action == "pressed":
            handle_events("up")
        elif event.direction == "down" and event.action == "pressed":
            handle_events("down")
        elif event.direction == "left" and event.action == "pressed":
            handle_events("left")
        elif event.direction == "right" and event.action == "pressed":
            handle_events("right")
        elif event.direction == "middle" and event.action == "pressed":
            handle_events("enter")

