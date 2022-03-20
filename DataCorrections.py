#! /usr/bin/env python3

import csv
import sys
import argparse

csvnamefile: str = "ex.csv"
newcsvnamefile: str  = "corrected_" + csvnamefile

class DataCorrections:
    def __init__(self):

        try:
            self.options = self.read_options(sys.argv[1:])
        except:
            print("Inpput Data file required...")
            exit(1)

        if self.options.input == None:
            print("[+] Please enter input/original data file\n")
            print(self.parser.print_help())
            exit(1)

        csvnamefile = self.options.input
        newcsvnamefile = csvnamefile[:-3] + "Corrected.csv"
        
        print("[+] Reading contents of input file: `{}`".format(csvnamefile))
        self.csvdatafile = csv.reader(open(csvnamefile, "r"))
        print("[+] Created output save file: `{}`".format(newcsvnamefile))
        self.newcsvdatafile = csv.writer(open(newcsvnamefile, "w"))

        print("[+] Data Processing....\nCorrections ongoing....\n[+] Please wait....")
        self.csvdata: list = list(self.csvdatafile)
        self.newcsvdata: list = self.csvdata
        self.num_rows: int = len(self.csvdata)

        # corrrections
        print("\n[+] Corrections on the Z-Axis distances")
        self.z_corrections()
        print("[+] Corrections on the distances range")
        self.range_corrections()

        self.newcsvdatafile.writerows(self.newcsvdata)
        print("[\n[+] Output file saved as: `{}`".format(newcsvnamefile))
        print("[+] Data Corrections Completed!!!\n")


    # declare function to define command-line arguments
    def read_options(self, args=sys.argv[1:]):
        """Returns dictionary of arguments values"""
        self.parser = argparse.ArgumentParser(description="The parsing commands lists.")
        self.parser.add_argument("input", help="Enter the original/input data file")
        return self.parser.parse_args(args)

    
    def range_corrections(self):
        minum: float = 30.0
        minad: float = 35.0
        maxum: float = 200.0
        maxad: float = 140.0

        for row in range(1, self.num_rows):
            r = float(self.csvdata[row][1])

            if r < minum:
                r = minad
            if r > maxum:
                r = maxad

            self.newcsvdata[row][1] = r

    
    def z_corrections(self):
        interval: float = 40.0

        for row in range(1, self.num_rows):
            z = float(self.csvdata[row][2])
            z = z * interval
            self.newcsvdata[row][2] = z


DataCorrections()

