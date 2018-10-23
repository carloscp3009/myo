# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 19:45:06 2018

@author: winston
"""
'''from __future__ import print_function

import enum
import re
import struct
import sys
import threading

import serial
from serial.tools.list_ports import comports

from common import *'''

import usb.core as core
import usb.util as util
import numpy as np
import csv
import os
import time

# Glove's USB identifiers
USB_VENDOR  = 0x5d70
L_iD = 0x0011
R_iD = 0x0010
USB_PRODUCT = 0
 

USB_IF      = 0     # Interface
USB_TIMEOUT = 500   # Timeout in MS
SLEEP_TIME  = 0.015 # Sampling interval
N_SAMPLES = 1000    

dev = None
Min = np.ones(5)*65536 #Vector with current minimum raw reading
Max = np.zeros(5)      #Vector with current maximum raw reading
flex_raw = np.zeros(5) #Vector with the latest raw reading
flex_cal = np.zeros(5) #Vector with the latest calibrated reading
  
def openPort(Vid,Pid,ifc):
    global dev
    #Find glove
    dev = core.find(idVendor=Vid, idProduct=Pid)
    #Return if glove isn't found
    if dev is None:
        return None
    #Claim interface
    if dev.is_kernel_driver_active(ifc) is True:
        dev.detach_kernel_driver(ifc)
    util.claim_interface(dev, ifc)
    return 0
    
def closePort(ifc):
    #Release interface
    util.release_interface(dev,ifc)

def readRaw():
    global Max
    global Min
    global flex_raw
    try:
        #Read encoded raw data from glove
        endpoint = dev[0][(0,0)][0]
        data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)
        #Decode raw data        
        flex_raw[0] = data[1]+(data[0]*256)
        flex_raw[1] = data[7]+(data[6]*256)
        flex_raw[2] = data[13]+(data[12]*256)
        flex_raw[3] = data[19]+(data[18]*256)
        flex_raw[4] = data[25]+(data[24]*256)
        #Update maximum and minimum values as needed
        Max = np.maximum(flex_raw,Max)
        Min = np.minimum(flex_raw,Min)
    except:
        pass

def readCal():
    global flex_cal
    readRaw()
    #Scale raw data with respect to current extreme values
    flex_cal = (flex_raw-Min)/(Max-Min)

#Calibration routine to get good initial extreme values    
def calibrate():
    for i in np.arange(400):
        readRaw()
        time.sleep(0.015)

def main():
    print("Trying to connect to glove...")
    #Try left glove then right
    hand = "L"
    if openPort(USB_VENDOR,L_iD,USB_IF) is None:
        hand = "R"
        if openPort(USB_VENDOR,R_iD,USB_IF) is None:
            print("Glove not found")    
            return -1
    print(str(hand) + " glove connected!")
    print("")
    user = input("Type the name of the user and press ENTER: ")
    print("")
    print("Please open and close your fingers several times during calibration")
    input("Press ENTER to begin")
    print("Calibrating...")
    calibrate()
    print("Done")
    input("Press ENTER to continue")
    stop = 1
    while stop!=0:
        os.system("clear")
        print("Write one of the following labels according to the hand gesture to record:")
        print("0.Thumb")
        print("1.index")
        print("2.middle")
        print("3.ring")
        print("4.pinky")
        print("5.clopen")
        print("6.grab")
        print("write 'test' to show data without saving")
        print("write 'exit' to close")    
        label = input("Chosen label: ")
        if label=="exit":
            stop = 0
        elif label=="test":
            for i in np.arange(N_SAMPLES):
                #Take a single sample
                os.system("clear")                
                readCal()
                row = flex_cal.tolist()
                print(str(row[4]))
        else:
            os.system("clear")
            input("Press ENTER to begin collecting data for: " + label)
            data_list = []
            # Read samples
            readCal()
            print("Collecting data... 0%...")
            #Take N_SAMPLES samples
            for i in np.arange(N_SAMPLES):
                #Take a single sample and add gesture, hand and username labels
                readCal()
                row = flex_cal.tolist()
                row.append(label)
                row.append(hand)
                row.append(user)
                #Add new sample to the list
                data_list.append(row[:])
                time.sleep(0.015)
                if i == int(N_SAMPLES*0.25):
                    print("Collecting data... 25%...")
                elif i == int(N_SAMPLES*0.5):
                    print("Collecting data... 50%...")
                elif i == int(N_SAMPLES*0.75):
                    print("Collecting data... 75%...")
            print("Collecting data... 100%...")
            # Save samples to CSV file
            with open("GloveData.csv","a") as csvFile:
                writer = csv.writer(csvFile)
                for i in data_list:
                    writer.writerow(i)
            csvFile.close()
                
    closePort(USB_IF)
    
if __name__ == '__main__':
    main()
