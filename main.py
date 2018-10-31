import threading
from myo_rawmdf import MyoRaw
from data_python2 import openPort, calibrate
from utils import save_arr_file
import os
import signal
import time

n = 0
label = None
stop = False
user = None


def myo_worker():
    global stop, label
    myo = MyoRaw(None)

    def log_emg(emg, a=None, b=None):
        global n
        print "[MYO]: " + emg
        save_arr_file(emg, 'emg_data.txt')
        n += 1

        if (n == 10):
            n = 0
            stop = True

    myo.add_emg_handler(log_emg)
    myo.connect()

    while not stop:
        myo.run(1)


def glove_worker():
    global label, user, stop
    hand = u"L"

    print "[GLOVE]: " + unicode(hand) + u" glove connected!"
    print "[GLOVE]: " + u"Calibrating..."
    calibrate()

    while not stop:
        print hand

    return


def main():
    global user, label, stop
    user = raw_input(u"Type the name of the user and press ENTER: ")

    myo_thread = Thread(target=myo_worker)
    glove_thread = Thread(target=glove_worker)
    # myo_thread.setDaemon(True)

    raw_input(u"Press ENTER to START")
    glove_thread.start()
    myo_thread.start()

    while not stop:
        os.system(u"clear")
        print u"1.index"
        print u"write 'exit' to close"
        label = raw_input(u"Chosen label: ")

        print label

        if label == u"exit":
            # glove_thread.
            # myo_worker = None
            stop = True

    return


class Job(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        # The shutdown_flag is a threading.Event object that
        # indicates whether the thread should be terminated.
        self.shutdown_flag = threading.Event()

        # ... Other thread setup code here ...

    def run(self):
        print('Thread #%s started' % self.ident)

        while not self.shutdown_flag.is_set():
            # ... Job code here ...
            time.sleep(0.5)

        # ... Clean shutdown code here ...
        print('Thread #%s stopped' % self.ident)

    def stop(self):
        self.shutdown_flag.set()
        self.join()


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit


def main_test():

    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    print('Starting main program')

    # Start the job threads
    try:
        j1 = Job()
        j1.start()

        i = 0
        # Keep the main thread running, otherwise signals are ignored.
        while i < 10:
            i += 1
            time.sleep(0.5)

        j1.stop()

    except ServiceExit:
        # Terminate the running threads.
        # Set the shutdown flag on each thread to trigger a clean shutdown of each thread.
        j1.shutdown_flag.set()
        # j2.shutdown_flag.set()
        # Wait for the threads to close...
        j1.join()
        # j2.join()

    print('Exiting main program')


if __name__ == '__main__':
    main_test()
