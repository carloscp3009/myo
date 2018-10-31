from threading import Thread
from myo_rawmdf import MyoRaw
from utils import *

n = 0


def myo_worker():
    myo = MyoRaw(None)

    def log_emg(emg, a=None, b=None):
        global n
        print emg
        save_arr_file(emg, 'emg_data.txt')
        n += 1

        if (n == 500):
            n = 0
            exit(0)

    myo.add_emg_handler(log_emg)
    myo.connect()

    while True:
        myo.run(1)


def main():
    myo_thread = Thread(target=myo_worker)
    # myo_thread.setDaemon(True)
    myo_thread.start()

    return


if __name__ == '__main__':
    main()
