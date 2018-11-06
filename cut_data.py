import numpy as np
from io import open

with open('./data/charlie/mano_completa/glove_data', 'r') as glove_data:
    with open('./data/charlie/mano_completa/myo_data', 'r') as myo_data:
        with open('./cut_data/myo', 'a') as myo_cut:
            with open('./cut_data/glove', 'a') as glove_cut:

                for glove in glove_data:

                    glove_number = glove[:13]
                    for myo in myo_data:

                        print glove, myo

                        myo_number = myo[:13]
                        
