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

N_DATA = 1000
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

    t0 = time.time()

    i = 0
    while i < N_DATA or time.time() < t0 + 1:

        row = readCal()
        # row = flex_cal.tolist()

        GLOVE_DATA.append(row[:])
        i += 1

    """
    for i in np.arange(N_DATA):
        row = readCal()
        # row = flex_cal.tolist()

        GLOVE_DATA.append(row[:])
        time.sleep(0.0012)
        #  time.sleep(0.015)
    """

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
    time.sleep(0.5)
    calibrate()

    logging.info('Conectando MYO')
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
    save_data_file(MYO_DATA, '%s/%s/%s/myo_data' % (path, name, label))
    save_data_file(GLOVE_DATA, '%s/%s/%s/glove_data' % (path, name, label))

    logging.warn('Terminando programa principal')


if __name__ == '__main__':

    """El programa debe ser ejecutado vía consola. Así:

        sudo python main.py <nombre> <label> <path>

        <nombre>:   nombre de la persona
        <label>:    nombre que recibirá el movimiento (index, ...)
        <path>:     path de la carpeta donde se guardarán los datos

        NOTA: Se crearán varias carpetas. Ejemplo:

        sudo python main.py wilson index ./data

        Se creará una carpeta 'data' en el directorio actual. Dentro de 'data' irá una carpeta
        llamada 'wilson', y dentro de ésta otra carpeta llamada 'index'

        ./data/wilson/index

    """

    args = sys.argv

    if not len(args) == 4:
        logging.error('Wrong arguments')
        exit()

    name = args[1]
    label = args[2]
    path = args[3]

    if not os.path.exists('%s/%s/%s' % (path, name, label)):
        os.makedirs('%s/%s/%s' % (path, name, label))

    main(name, label, path)
