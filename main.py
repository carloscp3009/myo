import threading
from myo_rawmdf import MyoRaw
from data_python2 import openPort, calibrate
from utils import save_arr_file
import os
import signal
import time

n = 0
LABEL = None
STOP = False
USER = None
DATA_N = 10


def glove_worker():
    global label, user, stop
    hand = u"L"

    print "[GLOVE]: " + unicode(hand) + u" glove connected!"
    print "[GLOVE]: " + u"Calibrating..."
    calibrate()

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
            # ... Job code here ...
            # self.print_message(self.name)
            # time.sleep(0.5)

            # ... Clean shutdown code here ...

    def stop(self):
        self.shutdown_flag.set()
        self.join()
        self.print_message('%s stopped' % self.name)

    def print_message(self, str):
        print '[%s]: %s' % (self.name, str)


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

    def __init__(self, name):
        Job.__init__(self, name)
        self.glove = None

    def data_adquisition(self):
        global user, label, stop
        hand = u"L"


def menu(myo, glove):

    global DATA_N, LABEL

    i = 0
    while True:

        i += 1

        print "[MAIN] 1. index"
        print "[MAIN] 0. exit"

        LABEL = int(raw_input('Label: '))
        os.system('clear')

        if LABEL == 0:
            # Stop the threads
            myo.stop()
            glove.stop()
            return


def main():

    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    print('[main]: Starting main program')

    # Start the job threads
    try:
        myo = MyoJob('myo')  # Myo Thread
        glove = GloveJob('glove')  # Glove Thread

        # Start the threads
        myo.start()
        glove.start()

        # Menu
        menu(myo, glove)

    except ServiceExit:
        myo.stop()
        glove.stop()

    print('[main]: Exiting main program')


if __name__ == '__main__':
    main()
