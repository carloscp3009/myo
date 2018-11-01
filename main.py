#!/usr/bin/python
# -*- coding: utf-8 -*-

from myo_rawmdf import MyoRaw
from data_python2 import openPort, calibrate, readCal, readRaw, flex_cal, flex_raw
from utils import save_arr_file
import os
import time
import signal
import logging
import threading
import numpy as np


logging.basicConfig(level=logging.DEBUG)

n = 0
LABEL = None
STOP = False
USER = None
DATA_N = 10

MYO_READY = True
GLOVE_READY = False

GLOVE_END = False


def glove_worker():
    global label, user, stop

    while not stop:
        print hand

    return


class Job(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.setName(name)
        self.shutdown_flag = threading.Event()

        # ... Other thread setup code here ...

    def run(self):
        self.print_message(u'%s started ' % self.name)

        while not self.shutdown_flag.is_set():
            pass
            # self.print_message(self.name)

            # ... Clean shutdown code here ...

    def stop(self):
        self.shutdown_flag.set()
        self.join()
        self.print_message('%s stopped' % self.name)

    def print_message(self, str):
        logging.info(str)


class ServiceExit(Exception):
    pass


def service_shutdown(signum, frame):
    print('[service_shutdown]: Caught signal %d' % signum)
    raise ServiceExit


class MyoJob(Job):
    """Myo thread class
    """

    def __init__(self, name):
        Job.__init__(self, name)
        self.myo = None


class GloveJob(Job):
    """Glove thread class
    """

    def __init__(self, name, hand):
        Job.__init__(self, name)
        self.glove = None
        self.hand = hand

    def init_glove(self):
        global GLOVE_READY

        self.print_message(
            "[GLOVE]: " + unicode(self.hand) + u" glove connected!")
        self.print_message("[GLOVE]: " + u"Calibrating...")
        calibrate()
        GLOVE_READY = True

    def run(self):
        global LABEL, DATA_N, USER, GLOVE_END
        self.print_message(u'%s started ' % self.name)

        while not self.shutdown_flag.is_set():
            if not GLOVE_READY:
                self.init_glove()

            print LABEL

            if LABEL == 1:
                data = self.read_data(LABEL, USER, DATA_N, self.hand)
                GLOVE_END = True

    def read_data(self, label, user, n, hand):
        data_list = []
        readCal()
        for i in np.arange(n):
                # Take a single sample and add gesture, hand and username labels
            readCal()
            row = flex_cal.tolist()
            row.append(label)
            row.append(hand)
            row.append(user)

            # Add new sample to the list
            data_list.append(row[:])
            time.sleep(0.015)
            if i == int(n*0.25):
                print u"Collecting data... 25%..."
            elif i == int(n*0.5):
                print u"Collecting data... 50%..."
            elif i == int(n*0.75):
                print u"Collecting data... 75%..."

        return data_list


def menu(myo, glove):

    global DATA_N, LABEL, USER, MYO_READY, GLOVE_READY, GLOVE_END

    USER = raw_input('[MAIN]: Digite el nombre: ')

    while True:

        if not MYO_READY or not GLOVE_READY:
            # print "Myo or Glove not ready..."
            continue

        print GLOVE_END

        if GLOVE_END:
            LABEL = -1

        print "[MAIN] 1. index"
        print "[MAIN] 0. exit"

        LABEL = int(raw_input('[MAIN]: Digite el número '))
        # os.system('clear')

        if LABEL == 0:
            # Stop the threads
            myo.stop()
            glove.stop()
            break


def main():

    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    logging.info('[main]: Iniciando programa principal')

    # Start the job threads
    try:
        myo = MyoJob('myo')  # Myo Thread
        glove = GloveJob('glove',  u"L")  # Glove Thread

        # Start the threads
        myo.start()
        glove.start()

        time.sleep(1)

        # Menu
        menu(myo, glove)

    except Exception as e:
        logging.error(e.message)
        myo.stop()
        glove.stop()

    logging.info('[main]: Saliendo del programa principal')


if __name__ == '__main__':
    main()
