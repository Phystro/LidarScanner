#! /usr/bin/env python3

import sys
import csv
import docx
import argparse


docname: str = "lidar.docx"
csvname: str = "lidar.csv"
header: list = ["θ", "r", "z"]
data = []

class DondoshaData:
    def __init__(self):

        try:
            self.options = self.read_options(sys.argv[1:])
        except:
            print("\n[-] Input data file required...\n")
            exit(1)

        if self.options.input == None:
            print("\n[-] Please enter input/original data file\n")
            print(self.parser.print_help())
            exit(1)

        docname = self.options.input
        csvname = docname[:-4] + "csv"

        try:
            self.doc = docx.Document(docname)
        except IOError:
            print("[-] Error opening file")
            return
        else:
            print("[+] Reading data from `{}` docx file".format(docname))
            for docsdata in self.doc.paragraphs:
                data.append(docsdata.text)
            
            print("[+] Created data output save file: `{}`".format(csvname))
            self.csvfile = csv.writer(open(csvname, "w"))

        
        print("[+] Data processing....\n[+] Please wait....")
        self.stats()
        csvdata = [ line.split(",") for line in data ]
        
        self.csvfile.writerow(header)
        self.csvfile.writerows(csvdata)

        print("[+] Output file saved as: `{}`".format(csvname))
        print("[+] Data Dondosha completed!!!\n")


    def stats(self):
        l = len(data)
        print("\n[+] Lines of Data: {}".format(l))

    # declare function to define command-line arguments
    def read_options(self, args=sys.argv[1:]):
        """Returns dictionary of arguments values"""
        self.parser = argparse.ArgumentParser(description="The parsing commands lists.")
        self.parser.add_argument("input", help="Enter the original/input data file")
        return self.parser.parse_args(args)
        
    
DondoshaData()

