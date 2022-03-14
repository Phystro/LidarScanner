#! /usr/bin/env python3

import sys
import csv
import time
import serial
import argparse


class SerialDataLogger:
    def __init__(self):
        # read the argument values
        options = self.read_options(sys.argv[1:])
        if options.port == None:
            print("[-] Arduino Port needed...\n")
            print(self.parser.print_help())
            exit(1)
        if options.baud == None:
            print("[-] Serial Baudrate needed...\n")
            print(self.parser.print_help())
            exit(1)

        # populate variables
        self.filename: str = "LidarScanCSVData.csv"
        self.logging: bool = False
        self.arduino_port: str = options.port
        self.baud: int = int(options.baud)

        try:
            # set up serial connection
            self.serial_connection = serial.Serial(self.arduino_port, self.baud)
        except (FileNotFoundError, serial.SerialException):
            print("[-] Incorrect or Non-Existing Arduino Port")
            sys.exit(2)
        else:
            print("[+] Connected to Arduino port: " + self.arduino_port + " @ baudrate: " + str(self.baud))
            self.logging = True
            # tell the serial port to clear the queue so that data doesn't overlap and create erroneous data points
            self.serial_connection.flushInput()
        finally:
            self.create_savefile()
        
        while self.logging:
            try:
                serial_bytes: bytes = self.serial_connection.readline()
            except serial.SerialException as e:
                self.logging = False
                print(e)
                sys.exit(2)
            except KeyboardInterrupt:
                print("[+] Program Terminated\n[+] Serial Data saved into 'LidarScannerData.csv' CSV file")
                exit(2)
            else:
                serial_data_string: str = serial_bytes.decode("UTF-8")
                self.serial_data: list = [data.strip("\t\n") for data in serial_data_string.split(",")]
                print(self.serial_data)

                with open(self.filename, "a") as f:
                    writer = csv.writer(f, delimiter=",")
                    writer.writerow(self.serial_data)
            finally:
                pass

    # declare function to define command-line arguments
    def read_options(self, args=sys.argv[1:]):
        """Returns dictionary of arguments values"""
        self.parser = argparse.ArgumentParser(description="The parsing commands lists.")
        self.parser.add_argument("-p", "--port", help="Enter the arduino port e.g. /dev/ttyUSB0")
        self.parser.add_argument("-b", "--baud", help="Enter the baudrate number")
        return self.parser.parse_args(args)
    
    def create_savefile(self):
        header = ["Theta", "Distance", "Z"]
        f = open(self.filename, "w")
        writer = csv.writer(f, delimiter=",")
        writer.writerow(header)
        f.close()

SerialDataLogger()
