#!/usr/bin/env python
import io
import os
import time
import datetime
import serial

from time import sleep        # to create delays

# from locale import format   # to format numbers PY2
import locale # PY3

from shutil import rmtree     # to remove directories

PathValid = False
FileName = ""
FilePath = ""
dataIndex = 0

FAIL_PATH = "/media/pi/USBDRIVE1/"
DRIVE_PATH = "/media/pi/USBDRIVE/"
AUTH_PATH = DRIVE_PATH + "validate.txt"

MAX_ROWS_IN_FILE = 65535

# main()
def chk_usb_on_start():
# validate_usb_write

    global PathValid, DRIVE_PATH, AUTH_PATH
    if not (os.path.exists(AUTH_PATH)):
        print("\n")
        print("To start datalogging, insert a usb drive that is formatted as FAT, with the ")
        print("label 'USBDRIVE', that has a text file named 'validate.txt' at the top level ")
        print("of the usb drive.\n")

        while not (os.path.exists(AUTH_PATH)):
            sleep(1)
            if (os.path.isdir(DRIVE_PATH)):
                if (os.path.isdir(FAIL_PATH)):
                    PathValid=True
                    validate_usb_write()
                    PathValid=False
                    print("To finish path correction, remove and replace USBDRIVE.")
                    
    print("'USBDRIVE' with 'validate.txt' file found.")

# validate_usb_write()
def set_path_invalid():

    global PathValid, dataIndex

    if not PathValid == False:
        PathValid = False
        print("USB path is not valid, corrupted, missing, or ejected")
        dataIndex = 0

# read_data()
def validate_usb_write():
# set_path_invalid

    global PathValid, DRIVE_PATH, AUTH_PATH

    if PathValid == False:
        return

    if not (os.path.exists(AUTH_PATH)):
        print("path corruption suspected")
        sleep(1)

        if not (os.path.exists(AUTH_PATH)):
            print("path corruption confirmed")
            print("validate.txt file was not found")
            set_path_invalid()

            rmtree(DRIVE_PATH, ignore_errors = True)

            if not (os.path.isdir(DRIVE_PATH)):
                print("path corruption corrected")

# read_data()
# main()
def start_new_file():
# set_path_invalid()

    global PathValid, FileName, FilePath, dataIndex

    FileName = str("_".join(str(datetime.datetime.now()).split(" ")))
    FileName = str("_".join(FileName.split(":")))
    FileName = str("_".join(FileName.split(".")))
    FileName = str("_".join(FileName.split("-")))
    FileName = FileName + ".csv"
    FilePath = DRIVE_PATH + FileName

    if (os.path.isdir(DRIVE_PATH)):
        mFile = open(FilePath, "w")
        print()
        print("#############################################################")
        print("New File: " + FileName)
        print("#############################################################")

        mFile.write("Index, Date, Time, Data \r\n")
        mFile.close()
        PathValid = True
        dataIndex = 1

    else:
        set_path_invalid();

# main()
def read_data():
# validate_usb_write()
# start_new_file()
# set_path_invalid()

    global PathValid, FileName, FilePath, dataIndex, ser

    if (PathValid == False):
        start_new_file()
        if (PathValid == False):
            return

    valueString = ""                  # reset the string that will collect chars
    
    #mchar = ser.read()               # PY2 read the next char from the serial port
    mchar = ser.read().decode()       # PY3
    
    while (mchar != '\n'):
        if (mchar != '\r'):
            valueString += mchar
        #mchar = ser.read()           # PY2
        mchar = ser.read().decode()   # PY3

    millis = int(round(time.time() * 1000))
    rightNow = str(datetime.datetime.now()).split()
    mDate = rightNow[0]
    mTime = rightNow[1]

    ## format the full string: index, timestamp, and data
    #locale.format_string('%05d', dataIndex) ## PY3
     
    #fileString = str(format('%05d', dataIndex)) + ", " + \
        #str(mDate) + ", " + str(mTime) + ", " + valueString
        
    fileString = locale.format_string('%05d', dataIndex) + ", " + \
        str(mDate) + ", " + str(mTime) + ", " + valueString

    try:
        if (os.path.exists(FilePath)):
            print(fileString)
            fileString += "\r\n"
            mFile = open(FilePath, "a", 1)
            mFile.write(fileString)
            mFile.close()
            dataIndex += 1
            validate_usb_write()
        elif (os.path.isdir(DRIVE_PATH)):
            start_new_file()
        else:
            set_path_invalid()
    except:
        print("write failed")
    if (dataIndex >= MAX_ROWS_IN_FILE):
        start_new_file()


def main():
# chk_usb_on_start()
# start_new_file()

    global ser
    ser = serial.Serial()
    ser.baudrate = 57600
    ser.timeout = None
    ser.port = '/dev/ttyACM0'
    print(ser)
    print(ser.name)
    ser.open()
    print("Serial port is open: ", ser.isOpen())

    chk_usb_on_start()
    start_new_file()

    try:
        while (True):
            read_data()
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
        print("Serial port is open: ", ser.isOpen())

    return 0

if __name__ == '__main__':
    main()
