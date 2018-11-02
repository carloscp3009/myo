from myo_rawmdf import MyoRaw


myo = MyoRaw(None)

j = 0
i = 0

def t(emg, a = None):
    global j
    print j, emg
    j += 1
    
myo.add_emg_handler(t)
myo.connect()


while i< 100:
    myo.run(100000)

    i += 1