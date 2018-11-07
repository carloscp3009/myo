import numpy as np
from io import open


glove_data = open('./data/charlie/mano_completa/glove_data', 'r')

myo_cut = open('./cut_data/myo', 'a')
glove_cut = open('./cut_data/glove', 'a')

for glove in glove_data:
    time_glove = glove[0:13]
    
    found = False
    myo_data = open('./data/charlie/mano_completa/myo_data', 'r')
    for myo in myo_data:
        time_myo = myo[0:13]
        
        if time_glove == time_myo:
            found = True
            
            if time_myo[-1] == ',':
                print(time_glove, time_myo)
                myo_cut.write(f'{myo[15:-3]}\n')
    
    if found:
        pass
