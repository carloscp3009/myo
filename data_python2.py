# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 19:45:06 2018

@author: winston 
"""
from __future__ import with_statement
from __future__ import division

from io import open
from utils import save_data_file

import usb.core as core
import usb.util as util
import numpy as np
import csv
import os
import time

# Glove's USB identifiers
USB_VENDOR = 0x5d70
L_iD = 0x0011
R_iD = 0x0010
USB_PRODUCT = 0

USB_IF = 0     # Interface
USB_TIMEOUT = 500   # Timeout in MS
SLEEP_TIME = 0.015  # Sampling interval
N_SAMPLES = 1000

dev = None
Min = np.ones(5)*65536  # Vector with current minimum raw reading
Max = np.zeros(5)  # Vector with current maximum raw reading
flex_raw = np.zeros(5)  # Vector with the latest raw reading
flex_cal = np.zeros(5)  # Vector with the latest calibrated reading


def openPort(Vid, Pid, ifc):
    global dev
    # Find glove
    dev = core.find(idVendor=Vid, idProduct=Pid)
    # Return if glove isn't found
    if dev is None:
        return None
    # Claim interface
    if dev.is_kernel_driver_active(ifc) is True:
        dev.detach_kernel_driver(ifc)
    util.claim_interface(dev, ifc)
    return 0


def closePort(ifc):
    # Release interface
    util.release_interface(dev, ifc)


def readRaw():
    global Max
    global Min
    global flex_raw
    try:
        # Read encoded raw data from glove
        endpoint = dev[0][(0, 0)][0]
        data = dev.read(endpoint.bEndpointAddress,
                        endpoint.wMaxPacketSize, USB_TIMEOUT)
        # Decode raw data
        flex_raw[0] = data[1]+(data[0]*256)
        flex_raw[1] = data[7]+(data[6]*256)
        flex_raw[2] = data[13]+(data[12]*256)
        flex_raw[3] = data[19]+(data[18]*256)
        flex_raw[4] = data[25]+(data[24]*256)
        # Update maximum and minimum values as needed
        Max = np.maximum(flex_raw, Max)
        Min = np.minimum(flex_raw, Min)

    except Exception as e:
        #  print e.args
        pass


def readCal():
    global flex_cal
    readRaw()
    # Scale raw data with respect to current extreme values
    flex_cal = (flex_raw-Min)/(Max-Min)

    return flex_cal


def calibrate():
    """Calibration routine to get good initial extreme values"""
    for i in np.arange(400):
        readRaw()
        time.sleep(SLEEP_TIME)
