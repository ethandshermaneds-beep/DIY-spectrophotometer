import RPi.GPIO as GPIO
import math
import time
import socket
import csv
import os
import subprocess
from datetime import datetime
from ADCDifferentialPi import ADCDifferentialPi

adc = ADCDifferentialPi(0x68, 0x68, 18)

remote_user = "Username" #Username on the controlling computer (not the rpi)
remote_host = "Hostname" #Hostname of the controlling computer
remote_path = "C:/Users/Username/path/to/directory" #where files will be written to on the controlling computer
local_dir = "/home/username" #directory on the rpi

spectrum = None
_current_file = None
_writer = None
_file_handle = None
_line_number = 0

STEP = 24
DIR = 23
DM0 = 17
DM1 = 27
DM2 = 22

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(DM0, GPIO.OUT)
GPIO.setup(DM1, GPIO.OUT)
GPIO.setup(DM2, GPIO.OUT)

GPIO.output(DM2, GPIO.HIGH)
GPIO.output(DM1, GPIO.LOW)
GPIO.output(DM0, GPIO.HIGH)

def blank(steps=150, delay=.01):
    global spectrum
    spectrum = []
    GPIO.output(DIR, GPIO.LOW)
    for _ in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(delay)
        voltage1 = adc.read_voltage(1)
        bar = int ((abs(voltage1) - .007) * 32768) #.007 is the ambient light level with the box lid closed
        if bar >= 150:
            bar = 0
        print(f"{voltage1:.6f} V","█" * bar)
        voltage2 = adc.read_voltage(1)
        voltage0 = (voltage1 + voltage2) / 2
        voltage = voltage0 - .007 #.007 is the ambient light level with the box lid closed
        spectrum.append(voltage)
    GPIO.output(DIR, GPIO.HIGH)
    for _ in range(abs(steps)):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(delay)

def step_motor(steps=150, delay=.01):
    GPIO.output(DIR, GPIO.LOW)
    for _ in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(delay)
        voltage1 = adc.read_voltage(1)
        bar = int ((abs(voltage1) - .007) * 32768) #.007 is the ambient light level with the box lid closed
        if bar >= 150:
            bar = 0
        print(f"{voltage1:.6f} V","█" * bar)
        voltage2 = adc.read_voltage(1)
        voltage0 = (voltage1 + voltage2) / 2
        voltage = voltage0 - .007 #.007 is the ambient light level with the box lid closed
        newline(voltage)
    GPIO.output(DIR, GPIO.HIGH)
    for _ in range(abs(steps)):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(delay)

def newfile():
    global _current_file, _writer, _file_handle, _line_number
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    _current_file = os.path.join(local_dir, f"{data}_{timestamp}.csv")
    _file_handle = open(_current_file, mode='w', newline='')
    _writer = csv.writer(_file_handle)
    _writer.writerow(["Index", "Timestamp", "Reading", "Reference", "Transmittance", "Absorbance"])
    _line_number = 0
    return _current_file

def newline(voltage):
    global _line_number, _writer, _file_handle, spectrum
    if spectrum is None:
        raise RuntimeError("No blank recorded")
    if _writer is None:
        raise RuntimeError("No file")
    Vref = spectrum[_line_number]
    _line_number += 1
    timestamp = datetime.now().isoformat()
    if Vref <= 0:
        T = None
        A = None
    else:
        T = voltage / Vref
        A = -math.log10(T) if T > 0 else None
    _writer.writerow([_line_number, timestamp, voltage, Vref, T, A])
    _file_handle.flush()

def sendfile(remote_user, remote_host, remote_path):
    global _current_file, _writer, _file_handle
    if _file_handle is None:
        raise RuntimeError("No file")
    _file_handle.close()
    scp_cmd = [
        "scp",
        _current_file,
        f"{remote_user}@{remote_host}:{remote_path}"
    ]
    result = subprocess.run(scp_cmd)
    if result.returncode == 0:
        os.remove(_current_file)
        print("file sent")
    else:
        print("file not sent")
    _current_file = None
    _writer = None
    _file_handle = None

HOST = ''
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
print("standby...")

try:
    while True:
        conn, addr = s.accept()
        data = conn.recv(1024).decode().strip()
        if data == "blank":
            print("")
            blank()
            conn.sendall(b"Blank complete")
        else:
            print("")
            newfile()
            step_motor()
            conn.sendall(b"Sample complete")
            sendfile(remote_user, remote_host, remote_path)
        conn.close()

finally:
    GPIO.output(DM2, GPIO.LOW)
    GPIO.output(DM1, GPIO.LOW)
    GPIO.output(DM0, GPIO.LOW)
