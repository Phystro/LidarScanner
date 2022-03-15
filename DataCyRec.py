#! /usr/bin/env python3

import sys
import csv
import argparse
import numpy as np

ROUND_OFF: int = 4
theta: float = 0.0
r: float = 0.0
z: float = 0.0
y: float = 0.0
x: float = 0.0

class DataConverter:
    def __init__(self):
        
        try:
            self.options = self.read_options(sys.argv[1:])
        except:
            print("Input data file required...")
            exit(1)

        if self.options.input == None:
            print("[+] Please enter the input/origianl data file\n")
            print(self.parser.print_help())        
            exit(1)
        
        self.INPUT_FILE_PATH: str = self.options.input
        self.OUTPUT_FILE_PATH: str = "Rec_LidarScanCSVData.csv"
        
        try:
            self.cylindrical_file = csv.reader(open(self.INPUT_FILE_PATH, "r"))
        except FileNotFoundError as e:
            print(e)
            exit(1)
        
        self.rectangular_file = csv.writer(open(self.OUTPUT_FILE_PATH, "w"))
        self.preport("Completed reading contents of file: " + self.INPUT_FILE_PATH)
        self.preport("Created data output save file: " + self.OUTPUT_FILE_PATH)

        self.cylindrical_data: list = list(self.cylindrical_file)
        self.rectangular_data: list = self.cylindrical_data

        self.num_rows: int = len(self.cylindrical_data)
        self.preport("Data processing has began...\n[+] Please wait..........")

        self.data_conversion()

        # Save the new file with elements in rectangular coordinates
        self.rectangular_file.writerows(self.rectangular_data)
        self.preport("Output file '" + self.OUTPUT_FILE_PATH + "' Saved.")
        self.preport("Data conversion completed!!!")


    # declare function to define command-line arguments
    def read_options(self, args=sys.argv[1:]):
        """Returns dictionary of arguments values"""
        self.parser = argparse.ArgumentParser(description="The parsing commands lists.")
        self.parser.add_argument("input", help="Enter the original/input data file")
        return self.parser.parse_args(args)


    def deg2rad(self, pembe: float) -> float:
        return (np.pi * pembe) / 180.0


    def preport(self, mesg: str):
        print("[+] " + mesg + " \r")

    
    def dreport(self, mesg: str):
        print("[-] " + mesg + "\r")
    

    def data_conversion(self):
        first_data_row_index = 0    
        
        if type(self.rectangular_data[0][0]) == str:
            first_data_row_index = 1
            self.rectangular_data[0][0] = "X"
            self.rectangular_data[0][1] = "Y"
            self.rectangular_data[0][2] = "Z"

        for row in range(first_data_row_index, self.num_rows):
            theta = float(self.cylindrical_data[row][0])
            r = float(self.cylindrical_data[row][1])
            z = float(self.cylindrical_data[row][2])

            theta = self.deg2rad(theta)

            x = round(r * np.cos(theta), 4)
            y = round(r * np.sin(theta), 4)
            z = round(z, 4)

            self.rectangular_data[row][0] = x
            self.rectangular_data[row][1] = y
            self.rectangular_data[row][2] = z
    
DataConverter()
