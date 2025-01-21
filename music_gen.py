# Automatic Music Generator File
#--------------------------------

#import all libraries
from music21 import *
import glob
from tqdm import tqdm
import numpy as np
import random
from tensorflow.keras.layers import LSTM, Dense, Input, Dropout
from tensorflow.keras.models import Sequential, Model, load_model
from sklearn.model_selection import train_test_split

def read_files(file):
    notes = []
    notes_to_parse = None
    
    # parse midi file
    midi = converter.parse(file)
    
    # seperate all instruments from the file
    instrmt = instrument.partitionByInstrument(midi)
    
    for part in instrmt.parts:
        # fetch only piano data
        if 'Piano' in str(part):
            notes_to_parse = part.recurse()
            
            # iterate over all parts of sub stream elements
            # check if element type is a note or chord
            # if it is a chord, split into notes
            for element in notes_to_parse:
                if type(element) == note.Note:
                    notes.append(str(element.pitch))
                elif type(element) == chord.Chord:
                    notes.append('.'.join(str(n) for n in element.normalOrder))
    # return list of notes
    return notes
    

#retreive paths recursively from inside the directories/files
file_path = ["schubert"]
all_files = glob.glob('All Midi Files/'+file_path[0]+'/.mid', recursive=True)

# reading eadh midi file
notes_array = np.array([read_files(i) for i in tqdm(all_files, position=0, leave=True)])

#create new notes using the frequent notes
#new_notes=[[i for i in j if i in freq_notes] for j in notes_array]


#unique notes
notess = sum(notes_array,[])
unique_notes = list(set(notess))
print("Unique Notes:",len(unique_notes))

#notes with their frequency
freq=dict(map(lambda x: (x,notess.count(x)),unique_notes))

#filter notes greater than threshold i.e. 50
#freq_notes=dict(filter(lambda x:x[1]>=50,freq.items()))

#get the threshold frequency
for i in range(30,100,20):
    print(i,":",len(list(filter(lambda x:x[1]>=i,freq.items()))))
    


