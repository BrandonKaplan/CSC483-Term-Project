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

###########################
######## CONSTANTS ########
###########################
VOWELS = ['AH0', 'EY1', 'AA2', 'IY0', 'AO2', 'OY1', 'AY1', 'OW2', 'EH2', 'IY1', 'AY2', 'OW1', 'ER0', 'UW1', 'IH1', 'IH0', 'IH2', 'AA1', 'AE2', 'EH1', 'AA0', 'AW1', 'AE1', 'OW0', 'AW2', 'EY2', 'EY0', 'AE0', 'IY2', 'ER1', 'EH0', 'UW2', 'AH1', 'AH2', 'AO0', 'OY2', 'OY0', 'UH1', 'AO1', 'UW0', 'AW0', 'AY0', 'ER2', 'UH0', 'UH2']
CONSONANTS = ['D', 'L', 'R', 'Z', 'S', 'V', 'B', 'K', 'T', 'G', 'N', 'M', 'P', 'W', 'DH', 'JH', 'NG', 'TH', 'ZH', 'SH', 'F', 'CH', 'HH', 'Y']


def main():

    # assign directory
    directory = 'output_folder'
     
    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        if (filename.endswith('.TextGrid')):
           
            f = os.path.join(directory, filename)
            read_textGrid(f, filename.split(".")[0])

    
'''
SUMMARY: Splits up the phonemes by reading neural network output

DESCRIPTION: Splits the phonemes into separate phoneme recording files based on the
TextGrid output of the neural network. This labels this file as the phoneme that the
neural network found
'''
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
            
            # mark is the phoneme name, mintime is the time it starts, maxtime is the time it ends
            print(interval.minTime)
            print(interval.maxTime)
            print(interval.mark)

'''
SUMMARY: Finds the amount of unique phonemes given a pronunciation dictionary
'''
def find_unique_phonemes():
    # constants for this function
    PHONEME_INDEX = 1

    # unique phonemes that are in the dictionary
    unique_phonemes = []

    # phonetic combinations
    phoneme_combos = []
    # number of words needed to say for unique combos
    word_count = 0

    # name of the pronunciation of file
    pronunciation_file_name = input("File for Unique phonemes: \n")
    pronunciation_file = open(pronunciation_file_name, "r")
    
    # iterates for all the words and pronunciations in the file
    for word_and_pronunciation in pronunciation_file:
        split_line = word_and_pronunciation.split()
        # the pronunciation text version for the word
        phonetic_pronunciation = split_line[PHONEME_INDEX:]

        quantity_to_add = 0
        for index in range(0, len(phonetic_pronunciation)):
            current_phoneme = phonetic_pronunciation[index]

            if (current_phoneme in VOWELS):
                # figures out if it is a unique phoneme
                if (current_phoneme not in unique_phonemes):
                    unique_phonemes.append(current_phoneme)
                
                if (index != 0):
                    prior_phoneme =  phonetic_pronunciation[index - 1]
                    phoneme_combination = prior_phoneme + "-" + current_phoneme + "(" + current_phoneme + ")"
                    
                    
                    if (phoneme_combination not in phoneme_combos):
                        quantity_to_add = 1
                        phoneme_combos.append(phoneme_combination)

                if (index < len(phonetic_pronunciation) - 1):
                    next_phoneme =  phonetic_pronunciation[index + 1]
                    phoneme_combination = current_phoneme + "-" + next_phoneme + "(" + current_phoneme + ")"
                    

                    if (phoneme_combination not in phoneme_combos):
                        quantity_to_add = 1
                        phoneme_combos.append(phoneme_combination)
        word_count = word_count + quantity_to_add

    print(unique_phonemes)
    print(len(unique_phonemes))
    print(phoneme_combos)
    print(word_count)
    print(len(VOWELS))
    print(len(CONSONANTS))

main()
