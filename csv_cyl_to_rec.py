import csv
import sys
import numpy as np

"""
Description: This script takes a csv file whose data is in rectangular coordinates
                and changes the elements of the file to values in rectangular coordinates
"""

# Constants
# path of file with input data
INPUT_FILE_PATH: str = "data.csv"
# path of file to write out the output data
OUTPUT_FILE_PATH: str = "rec_data.csv"

ROUND_OFF: int = 4


def deg2rad(pembe: float) -> float:
    return (np.pi * pembe) / 180.0

def report(mesg: str):
    print("[+] " + mesg + " \r")

def main():
    # Coordinates
    theta: float = 0.0
    r: float = 0.0
    z: float = 0.0
    y: float = 0.0
    x: float = 0.0

    # Prepare
    cylindrical_file = csv.reader(open(INPUT_FILE_PATH))
    rectangular_file = csv.writer(open(OUTPUT_FILE_PATH, "w"))
    report("Read file: " + INPUT_FILE_PATH)
    report("Created file: " + OUTPUT_FILE_PATH)

    cyl_data: list = list(cylindrical_file)
    rec_data: list = cyl_data

    num_rows: int = len(cyl_data)
    
    report("Data processing has began...\nPlease Wait.....")
    
    for row in range(0, num_rows):
        theta = float(cyl_data[row][0])
        r = float(cyl_data[row][1])
        z = float(cyl_data[row][2])

        theta = deg2rad(theta)

        x = round(r * np.cos(theta), 4)
        y = round(r * np.sin(theta), 4)
        z = round(z, 4)

        rec_data[row][0] = x
        rec_data[row][1] = y
        rec_data[row][2] = z

        #print("Processing line " + str(row) + " of " + str(num_rows) + "\r")
    
    # Save the new file with elements in rectangular coordinates
    rectangular_file.writerows(rec_data)
    report("Output file " + OUTPUT_FILE_PATH + " Saved.")


# run program
main()
report("Data processing finished.")
