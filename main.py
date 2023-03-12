from sense_hat import SenseHat
from gpiozero import CPUTemperature
from datetime import datetime
import sys
from ISStreamer.Streamer import Streamer
import time
import math
sense = SenseHat()
bkey = "2fb27f6a-84c8-44c5-9c6e-3d61da431579"
key = "ist_1cvQJOd60hKx0j_IViCDjwXp-rdHl4MB"
logger = Streamer(bucket_name="RPI SENSE HAT DATA", bucket_key=bkey, access_key=key)
print(logger.log("TEST", 33))
white = (128,128,128)
red = (128,0,0)
off = (0,0,0)

flashon = False

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
#flashlight()

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

#sense.show_message(f'Temp is: {gettemp()}')
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

