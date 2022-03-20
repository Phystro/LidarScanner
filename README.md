<h1 align="center"> LidarScanner </h1>

<p align="center">
    Lidar scanner arduino project
</p>


**Description:**

Performs Lidar scan of a geological mines, creating a cylindrical set of codes, that we later convert into rectangular set of coordinates.


**Stepper Motor:**

Using 28BYJ-48 Stepper Motor with ULN2003 Driver and Arduino. The 28BYJ-48 is a 5-wire unipolar stepper motor. There are 2037.8864 ~ 2038 steps per revolution.

---

### Modules Needed

Install the following python modules first: `csv`, `serial`, `python-docx` and `pyserial`

```sh 
$ pip install csv serial pyserial python-docx
```


---
## Read from Serial Monitor and save into CSV file

The file `SerialDataLogger.py` reads serial data from the arduino serial monitor in real time and saves the data in a csv file format. The generated output file in saved as `LidarScanCSVData.csv`

### How to run it

You can find help or usage info by running:
```sh
$ python SerialDataLogger.py -h
```
or
```sh
$ python SerialDataLogger.py --help
```

Examples of executing the file:
```sh
$ python SerialDataLogger.py -p /dev/ttyUSB0 -b 115200
```
or
```sh
$ python SerialDataLogger.py --port /dev/ttyACM0 --baud 9600
```

---

## Convert Data from Cylindrical coordinates $(\theta, r, z)$ to Rectangular coordinates $(x, y, z)$

The file `DataCyRec.py` reads the csv data file and converts the cylindrical coordinates into rectangular coordinates, saving them in output file `LidarScanCSVData.Rec.csv`

### How to run it

Get help of usage info by running:
```sh
$ python DataCyRec.py -h
```
or
```sh
$ python DataCyRec.py --help
```

Examples of executing the file:
```sh
$ python DataCyRec.py sample_data.csv
```

---

