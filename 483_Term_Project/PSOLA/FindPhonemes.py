'''
AUTHOR: Hazel (Brandon) Kaplan
CLASS: CSC 483 - Text Retrieval and Web Search
ASSIGNMENT: Term Project
DESCRIPTION: Finds the phonemes in the audio file by reading in the text grid
output from the PSOLA algorithm and forced alignment neural network

'''
import textgrid
# imports the audio library
from pydub import AudioSegment, silence
import numpy as np
# imports for folder management
import os

def main():

    # assign directory
    directory = 'output_folder'
     
    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        if (filename.endswith('.TextGrid')):
           
            f = os.path.join(directory, filename)
            read_textGrid(f, filename.split(".")[0])

    
    
def read_textGrid(filepath, word):
    print(word)
    # contructs the file path for the subject
    word_audio_path = "input_folder/" + word + ".wav"
    
    # gets the pronunciation as the form of an AudioSegment
    word_audio = AudioSegment.from_file(word_audio_path, format='wav')

    # Read a TextGrid object from a file.
    tg = textgrid.TextGrid.fromFile(filepath)

    # Read a IntervalTier object.
    print("------- IntervalTier Example -------")
    print(tg[1])
    print(tg[1].intervals)

    for interval in tg[1].intervals:
        # does not create a phoneme for silence
        if (interval.mark != ""):
            startTime = interval.minTime * 1000
            endTime = interval.maxTime * 1000
            phoneme_audio = word_audio[startTime : endTime]
            full_path = "phonemes/" + interval.mark + ".wav"
            phoneme_audio.export(full_path, format="wav")
            
            print(interval.minTime)
            print(interval.maxTime)
            print(interval.mark)
main()
