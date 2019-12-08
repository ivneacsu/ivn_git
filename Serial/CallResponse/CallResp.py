import serial
port = "/dev/ttyACM0"
ser = serial.Serial(port)
import time

firstContact = False;
n = 8

while n >= 0:

  if (firstContact == False):
    inByte = ser.read(1).decode();
    if (inByte == 'A'):
      ser.flushInput();
      firstContact = True;
      ser.write(b'A'); ## ask for data
      inByte = '';
      
  else:
    time.sleep(1);
    ser.write(b'A');
    if ser.inWaiting() >= 3:
      inByte = ser.read(3);
      print(inByte)
      ser.flushInput()
      time.sleep(.005)
      n = n -1
    
#print("finish")
ser.close()
print("serial closed!")


