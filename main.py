#!/usr/bin/python
# -*- coding: utf-8 -*-

from myo_rawmdf import MyoRaw
from data_python2 import calibrate, closePort, readCal, readRaw, flex_cal, R_iD, USB_IF, L_iD, openPort, USB_VENDOR
from utils import save_arr_file, save_data_file
import os
import time
import signal
import logging
import threading
import sys
import numpy as np

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] - %(threadName)s \t:: %(message)s')

n = 0

myo = MyoRaw(None)

N_DATA = 100
MYO_COUNT = 0
GLOVE_COUNT = 0

MYO_DATA = []
GLOVE_DATA = []


def myo_worker():
    global myo, N_DATA, MYO_COUNT, MYO_DATA

    logging.info('Iniciando lectura de MYO')
    while MYO_COUNT < N_DATA:
        myo.run(1)

    myo.disconnect()
    logging.info('MYO DONE')


def glove_worker():
    global GLOVE_DATA
    logging.info('Iniciando lectura de GLOVE')

    readCal()

    for i in np.arange(N_DATA):
        row = readCal()
        # row = flex_cal.tolist()

        GLOVE_DATA.append(row[:])
        time.sleep(0.015)
        #  time.sleep(0.015)

    #  closePort(USB_IF)

    logging.info('GLOVE DONE')


def myo_data_proc(emg, a=None):
    global MYO_COUNT, MYO_DATA
    MYO_DATA.append(emg)
    MYO_COUNT += 1


def main(name, label, path):
    global myo, MYO_DATA

    hand = u"L"
    if openPort(USB_VENDOR, L_iD, USB_IF) is None:
        hand = u"R"
        if openPort(USB_VENDOR, R_iD, USB_IF) is None:
            logging.error('Glove not found')
            exit(-1)

    logging.info('Calibrando GLOVE')
    calibrate()

    myo.add_emg_handler(myo_data_proc)
    myo.connect()

    logging.info('Iniciando hilos')
    myo_thread = threading.Thread(target=myo_worker, name='myo')
    glove_thread = threading.Thread(target=glove_worker, name='glove')

    myo_thread.start()
    glove_thread.start()

    myo_thread.join()
    glove_thread.join()

    logging.info('Guardando datos')
    save_data_file(MYO_DATA, '%s/%s/myo_data' % (path, label))
    save_data_file(GLOVE_DATA, '%s/%s/glove_data' % (path, label))

    logging.warn('Terminando programa principal')


if __name__ == '__main__':

    args = sys.argv

    if len(args) < 4:
        logging.error('Missing arguments')
        exit()

    print args

    name = args[1]
    label = args[2]
    path = args[3]

    main(name, label, path)
