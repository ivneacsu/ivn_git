## https://gist.github.com/Marzogh/723c137a402be7f06dfc1ba0b8517d09
## adapted for pyduino

import serial
import csv
import re
import sys
import time ## my

# import matplotlib.pyplot as plt
# import pandas as pd
 
portPath = "/dev/ttyACM0"
baud = 9600
timeout = 5
filename = "data.csv"
max_num_readings = 5
num_signals = 1

analog_pin = 5               ## my
 
def create_serial_obj(portPath, baud_rate, tout):
    return serial.Serial(portPath, baud_rate, timeout = tout)
    
def read_serial_data(serial):

    time.sleep(1)            ## my
    serial.flushInput()   
    serial_data = []
    readings_left = True
    timeout_reached = False
    
    cmd = (''.join(('RA', str(analog_pin)))).encode() ## my
    
    while readings_left and not timeout_reached:
    
        ## pyduino (firmata ???)
        serial.write(bytes(cmd))          ## my
        #serial.write(b'RA0')             ## my, OK!
        time.sleep(0.1)                   ## my
        serial_line = serial.readline()   ## OK
        
        #serial_line = serial.read(serial.in_waiting).decode() ## ???
        
        if serial_line == '':
            timeout_reached = True
        else:
            serial_data.append(serial_line)
            if len(serial_data) == max_num_readings:
                readings_left = False
                
    serial.close()              ## my  
    return serial_data
 
def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
        
def clean_serial_data(data):
    """
    Give like: ['0.5000,33\r\n', '1.0000,283\r\n']
    Returns:   [[0.5,33.0], [1.0,283.0]]
    
               [b'A5:543\r\n', b'A5:345\r\n']
               []
    """
    clean_data = []
    
    for line in data:
        '''
        ## OK!
        line = line.decode()                        ## my: Py3        
        line_data = re.findall("\d*\.\d*|\d*",line) ## only digits
        line_data = [float(element) for element in line_data if is_number(element)]       
        if len(line_data) >= 2:
            #clean_data.append(line_data[1])
            clean_data.append(line_data)
        ## end OK
        '''
        
        #'''
        ## or:
        line_data = line.decode().strip().split(':')     ## OK!
        #print(line_data)       
        if len(line_data) > 1:
            clean_data.append(line_data)
        ## end or
        #'''
        
    return clean_data           
 
def save_to_csv(data, filename):

    #if sys.version_info >= (3,0,0):
        #f = open(filename, 'w', newline='')
    #else:
        #f = open(filename, 'wb')
        
    #with open(filename, 'wb') as csvfile:             ### Py2
    with open(filename, 'w', newline = '') as csvfile: ### Py3
        csvwrite = csv.writer(csvfile)           
        csvwrite.writerows(data)
 
def gen_col_list(num_signals):
    """
    E.g. 3 signals returns : ['Time','Signal1','Signal2','Signal3']
    """
    col_list = ['Time']
    for i in range(1,num_signals+1):
        col = 'Signal'+str(i)
        col_list.append(col)
        
    return col_list
    
def map_value(x, in_min, in_max, out_min, out_max):
    return (((x - in_min) * (out_max - out_min))/(in_max - in_min)) + out_min
    
def simple_plot(csv_file, columns, headers):
    plt.clf()
    plt.close()
    plt.plotfile(csv_file, columns, names=headers, newfig=True)
    plt.show()
 
def plot_csv(csv_file, cols):
    data_frame = pd.read_csv(csv_file)
    data_frame.columns = cols
    data_frame = data_frame.set_index(cols[0])
    # Map the voltage values from 0-1023 to 0-5
    data_frame = data_frame.apply(lambda x: map_value(x,0.,1023,0,5))
    # Bring back the Time column
    data_frame = data_frame.reset_index()
    plt.clf()
    plt.close()
    data_frame.plot(x=cols[0],y=cols[1:])
    plt.show()
    
print("Creating serial object...")
serial_obj = create_serial_obj(portPath, baud, timeout)
print("Serial port is open ?: ", serial_obj.is_open) ## my
 
print("Reading serial data from puduino.ino")
serial_data = read_serial_data(serial_obj)
print(len(serial_data))
print(serial_data)
 
print("Cleaning data...")
clean_data =  clean_serial_data(serial_data)
#print(clean_data)
 
print("Saving to data.csv")
save_to_csv(clean_data, filename)

print('Serial port is open ?: ', serial_obj.is_open) ## my

print("Plotting data ?")
#simple_plot(filename, (0,1,2), ['time (s)', 'voltage1', 'voltage2'])
#simple_plot(filename, (0,1), ['time (s)', 'voltage1'])
#plot_csv(filename, gen_col_list(num_signals))