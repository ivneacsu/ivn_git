#!/usr/bin/python
from sense_hat import SenseHat
import os,sys
import json
import urllib2
import datetime
import time

import IssFlags

sense = SenseHat()
flags = IssFlags

url1 = 'https://api.wheretheiss.at/v1/satellites/25544'
url2 = 'https://api.wheretheiss.at/v1/coordinates/'

URL_FOUND = False

red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (231, 255 , 7)
orange = (255,196,0)
color = black

sense.set_rotation(180)

def trackISS():
    global URL_FOUND

    data1 = getLocationISS()
    if URL_FOUND:
        data2 = processResponse(data1)
    time.sleep(45) ### default 10
    sense.clear(black)

def getLocationISS():
    global URL_FOUND

    try:
        response = json.load(urllib2.urlopen(url1))
    except urllib2.URLError as e:
        URL_FOUND = False
        text = "No response of ESA api !!"
        sense.show_message(text,text_colour=white,back_colour=red)
        sense.clear(black)
    else:
        URL_FOUND = True
        return response

def processResponse(response):
    global url2

    latitude = response['latitude']
    longitude = response['longitude']

    latitudeStr = str(latitude)
    longitudeStr = str(longitude)
    url3 = url2 + latitudeStr + ',' + longitudeStr     

    latitude = round(latitude, 1)
    longitude = round(longitude, 1)

    if latitude <0:
        lat = " S"
    else:
        lat = " N"
    if longitude <0:
        lng = " W"
    else:
        lng = " E"

    latitude = abs(latitude)
    longitude = abs(longitude)

    latStr = str(latitude) + lat
    lngStr = str(longitude) + lng

    light =  response['visibility']
    
    # Call 2nd API (is above land ??)
    try:
        response2 = json.load(urllib2.urlopen(url3))
    except urllib2.HTTPError as e:
        text = str("Sea %s %s %s" % ( latStr, lngStr, light ))
        sense.show_message(text,text_colour=white,back_colour=blue)
        sense.clear(black)
    except urllib2.URLError as e:
        text = "No response of ESA api !!"
        sense.show_message(text,text_colour=white,back_colour=red)
        sense.clear(black)
    else:
        countryCode = response2['country_code']
        string = response2['timezone_id']
        splitString = string.split("/")
        timeZone = splitString[1]
        flags.findFlag(countryCode,timeZone,light)

def text(text, color):
    
    sense.show_message(text, text_colour=color)
    
def endScript(color):
    text("Shutdown ..... ", color)
    sense.clear(black)
    sys.exit(0)

text("RPi", white)
text("SH", red)
text("RPi", blue)
text("SH", green)

if __name__ == "__main__":
    while True:
        try: 
            trackISS()
        except (KeyboardInterrupt):
            #endScript(red)
            sense.clear()
            sys.exit(0)
