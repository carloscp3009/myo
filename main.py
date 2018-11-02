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


def glove_worker():
    global label, user, stop
    hand = u"R"

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

    def __init__(self, name):
        threading.Thread.__init__(self)

        self.setName(name)

        # The shutdown_flag is a threading.Event object that
        # indicates whether the thread should be terminated.
        self.shutdown_flag = threading.Event()

        # ... Other thread setup code here ...

    def run(self):
        print('[THREAD] #%s started \n' % self.name)

        while not self.shutdown_flag.is_set():
            # ... Job code here ...
            print self.name
            time.sleep(0.5)

        # ... Clean shutdown code here ...

    def stop(self):
        self.shutdown_flag.set()
        self.join()
        print('[THREAD] #%s stopped \n' % self.name)


class ServiceExit(Exception):
    pass


def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit


class MyoJob(Job):
    def __init__(self, name):
        Job.__init__(self, name)

        self.myo = MyoRaw(None)
        self.myo.add_emg_handler(self.log_emg)
        self.myo.connect()

    def log_emg(self, emg):
        print "[MYO]: " + emg
        save_arr_file(emg, 'emg_data.txt')

    def run(self):
        print self.myo.arm_handlers


def main_test():

    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    print('Starting main program')

    # Start the job threads
    try:
        # j1 = Job('hola we')
        # j1.start()

        mj = MyoJob('haeh')
        mj.start()

        i = 0
        # Keep the main thread running, otherwise signals are ignored.
        while i < 10:
            i += 1
            time.sleep(0.5)

        mj.stop()

    except ServiceExit:
        # Terminate the running threads.
        mj.stop()

    print('Exiting main program')


if __name__ == '__main__':
    main_test()
