#! /usr/bin/env python3

import serial
import csv
import sys
import time

# constants and variables
arduino_port: str = "/dev/ttyUSB0"
baud: int = 115200
filename: str = "LidarScannerData.csv"

# Set up serial connection
ser = serial.Serial(arduino_port, baud)
#ser.flushInput()
print("Connected to Arduino port: " + arduino_port + "@" + str(baud))

header = ["Theta", "Distance", "Z"]
f = open(filename, "w")
writer = csv.writer(f, delimiter=",")
writer.writerow(header)
f.close()

def list_to_string(s):
    str1 = ",".join(s)
    return str1

while True:
    try:
        ser_bytes = ser.readline() # in bytes data type
        data_str = ser_bytes.decode("utf-8")
        data_strl = data_str.split(",")
        data_list = [d.strip("\t\n") for d in data_strl]
        data = data_list#list_to_string(data_list)
        
        print(data)
        with open(filename, "a") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(data)
    except:
        print("Keyboard Interrupt")
        break
    finally:
        pass

