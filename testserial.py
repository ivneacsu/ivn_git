#!/usr/bin/python
import serial
import sys
import time
ser = serial.Serial()
ser.port = "/dev/ttyACM0"
ser.baudrate = 9600
ser.timeout = 1
try:
    ser.open()
except Exception,e:
     print "byby!" + str(e)
     sys.exit(0)
if ser.isOpen():
    ser.flushInput()
while 1:
    try:
        while (ser.inWaiting() == 0):
            pass
        data = ser.readline().rstrip()
        print(data)
    except Exception,e2:
        print "wrong!" +str(e2)
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)
sys.exit(0)
