'''
AUTHOR: Hazel (Brandon) Kaplan
CLASS: CSC 483 - Text Retrieval and Web Search
ASSIGNMENT: Term Project
DESCRIPTION: Creates artificial pronunciations of words for a single set of phoneme recordings.
These artificial recordings are stored in a folder that is stores all the words in a wav audio
format. This program first takes in a name of the file that has a list of all the phonemes that
the program is using to generate the pronunciations, it then takes a name of the subject (folder
name) that contains all the recordings of the phonemes. Then it takes in one last additional file
which contains all the pronunciations in a text format that will have an artificial recording
be generated from

FILE SYSTEM STRUCTURE:
    483_Term_Project:
        This program
        phoneme_list.txt
        phonetic_pronunciations.txt
        Recordings:
            Subject One
                phoneme_one.wav
                phoneme_two.wav
                ...
            Subject Two
            Subject Three
            ...
        Artificial Data:
            Subject One
                word_one.wav
                word_two.wav
                ...
            Subject Two
            Subject Three
            ...
        ...
        

INPUT FILE FORMAT:

    PHONEME FILE:
    The file with the used phonemes should have one phoneme per line and use all caps:
    AE
    K
    IY
    IH
    ...

    PRONUNCIATION FILE:
    The file used for the pronunciations should be formatted as follows:
    BEEF	B IY F
    CUTE	K Y UW T
    TIRED	T AY ER D
    DEPRESSED	D IH P R EH S T
    MOTIVATION	M OW T AH V EY SH AH N
    APPLE	AE P AH L
    SAD	S AE D
    PERSEVERE	P ER S AH V IH R
    WORK	W ER K


DEVELOPER TECHNICAL DOCUMENTATION:
- The phoneme is assumed to be in the same directory as this program is located in
- "Subject" refers to the person that the program is contructing the artificial data for
- Must have the PyDub library installed for this program to work, run "pip install pydub"
  in the terminal
  
'''


# imports the audio library
from pydub import AudioSegment, silence
import numpy as np
# imports for folder management
import os

'''
SUMMARY: Creates a single artificial pronunciation of a word

DESCRIPTION: Given a pronunciation of a word, this function creates an artificial pronunciation
by adding the segments of audio to build the full pronunciation from the pronunciation
dictionary

PARAMETERS:
    - phonetic_pronunciation: Python list of phonemes which are strings
    - pronunciation_dictionary: dictionary that maps phoneme strings to the AudioSegment
    pronunciation from the subject

'''
def create_artificial_word(phonetic_pronunciation, pronunciation_dictionary):
    # creates an empty AudioSegment to add phonemes to
    artificial_word = AudioSegment.empty()
    # iterates through the pronunciations
    for phoneme in phonetic_pronunciation:
        # looks up the AudioSegment in the pronunciation_dictionary
        phoneme_audio = pronunciation_dictionary[phoneme]
        # adds/builds the AudioSegment by adding the audio
        artificial_word += phoneme_audio
    return artificial_word
    

'''
SUMMARY: Creates the artificial pronunciationa of each of the words

DESCRIPTION: Opens the file with the pronunciations for the various words, goes through them
all, then creates an artificial pronunciation of the word using the phoneme dictionary for the
subject. This is all written in one function but uses other functions to prevent having to loop
through the dictionary twice O(N^2) if it were to just get the pronunciation content first. This
function then exports the artifiical data created to an Artificial Recordings folder with the
subject's name and store every word there. 

PARAMETERS:
    - pronunciation dictionary: A dictionary that maps the phoneme string to the AudioSegment
    type recording of the subjects phoneme
    - subject_name: String that is the name of the directory of the subjects recordings
'''
def create_artificial_data(subject_name, pronunciation_dictionary, pitch_shift):
    # constants for this function
    WORD_INDEX = 0
    PHONEME_INDEX = 1

    # format for the folders and output
    result_format = input("Write either 'test' or 'nn' for neural network format: \n")
    
    # gets the name and opens the file with the words with their phonetic pronunciations
    word_file_name = input("Enter name of the file that contains the words and their phonetic" \
                    + " pronunciations: \n")
    word_file = open(word_file_name, "r")

    # iterates for all the words and pronunciations in the file
    for word_and_pronunciation in word_file:
        split_line = word_and_pronunciation.split()
        # word that the program is constructing artifical data for
        word = split_line[WORD_INDEX]
        # the pronunciation text version for the word
        phonetic_pronunciation = split_line[PHONEME_INDEX:]
        # gets the artificial pronunciation AudioSegment of the word
        artificial_pronunciation = create_artificial_word(phonetic_pronunciation, pronunciation_dictionary)

        if (result_format == "test"):
            # creates the path exports the artificial file to the directory
            artificial_storage_path = "Artificial Pronunciations/" + subject_name + "/" + word + ".wav"
            artificial_pronunciation.export(artificial_storage_path, format="wav")

            # convert the audio to single channel
            sound = AudioSegment.from_wav(artificial_storage_path)
            sound = sound.set_channels(1)
            sound.export(artificial_storage_path, format="wav")

        elif (result_format == "nn"):
            neural_storage_path = "NN Format/" + word + "/" 
            # checks if the folder/directory does not exist yet
            if (not os.path.exists(neural_storage_path)):
                # creates the directory if it does not exist
                os.mkdir(neural_storage_path)
                
            file_number = 0
            full_path = neural_storage_path + word + str(file_number) + ".wav"
            # loops till it finds a unique name for file
            while (os.path.isfile(full_path)):
                file_number = file_number + 1
                full_path = neural_storage_path + word + str(file_number) + ".wav"

            # exports the artificial file to the neural directory
            artificial_pronunciation.export(full_path, format="wav")

            # pitch shift the word up
            if(pitch_shift == "True"):
                filename = neural_storage_path + word + str(file_number) + ".wav"
                out_path = neural_storage_path + word + str(file_number + 1) + ".wav"

                sound = AudioSegment.from_file(filename, format="wav")
                octaves = 0.25
                new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
                hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
                hipitch_sound = hipitch_sound.set_frame_rate(4800)
                hipitch_sound.export(out_path, format="wav")
                sc = AudioSegment.from_file(out_path, format="wav")
                sc = sc.set_channels(1)
                sc.export(out_path, format="wav")
            
            # pitch shift the word down
            if(pitch_shift == "True"):
                filename = neural_storage_path + word + str(file_number) + ".wav"
                out_path = neural_storage_path + word + str(file_number + 2) + ".wav"

                sound = AudioSegment.from_file(filename, format="wav")
                octaves = -0.25
                new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
                hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
                hipitch_sound = hipitch_sound.set_frame_rate(4800)
                hipitch_sound.export(out_path, format="wav")
                sc = AudioSegment.from_file(out_path, format="wav")
                sc = sc.set_channels(1)
                sc.export(out_path, format="wav")

            # convert to single channel
            sound = AudioSegment.from_wav(full_path)
            sound = sound.set_channels(1)
            sound.export(full_path, format="wav")
        else:
            print("Invalid file format, please try again")
    return 


'''
SUMMARY: Creates a pronunciation dictionary of the subject's phonemes

DESCRIPTION: Using a list of phonemes, this function creates a pronunciation dictionary by
mapping the string phoneme to an AudioSegment that contains the subject's pronunciation for
that phoneme

PARAMETERS:
    - subject_name: String that is the name of the directory of the subjects recordings
    - phoneme_list: Python list of the phonemes in all caps
    
RETURNS:
    - pronunciation_dictionary: Dictionary containing the phonemes as keys and the AudioSegment
    of the subjects pronunciation of that phoneme
'''
def get_pronunciation_dictionary(subject_name, phoneme_list, norm):
    pronunciation_dictionary = {}

    # goes through each of the phoneme_list
    for phoneme in phoneme_list:
        # contructs the file path for the subject
        pronunciation_file_path = "Trimmed Recordings/" + subject_name + "/" + phoneme + ".wav"
        # gets the pronunciation as the form of an AudioSegment
        phonetic_pronunciation = AudioSegment.from_file(pronunciation_file_path, format='wav')

        # normalize the decimal level
        if(norm == "True"):
            target_decible_level = -20
            current_volume = phonetic_pronunciation.dBFS
            needed_gain = target_decible_level - current_volume
            normalized_file_path = "Norm/" + subject_name + "/" + phoneme + ".wav"

            if(current_volume < target_decible_level):
                # apply the needed volume adjustment to the phoneme
                new_volume = phonetic_pronunciation.apply_gain(needed_gain)
                new_volume.export(normalized_file_path, format="wav")
            else:
                phonetic_pronunciation.export(normalized_file_path, format="wav")
            
            normalized_phoneme_pronunciation = AudioSegment.from_file(normalized_file_path)
            pronunciation_dictionary[phoneme] = normalized_phoneme_pronunciation
        else:
            # maps the phoneme to the AudioSegment pronunciation
            pronunciation_dictionary[phoneme] = phonetic_pronunciation

    return pronunciation_dictionary


'''
SUMMARY: Reads in a list of phonemes that will be used that are in the pronunciations

DESCRIPTION: Takes in a file name through input and then reads the entire list of phonemes
that are stated in the file. This also strips off the newline characters for easy matching
in the future when contructing a pronunciation dictionary

RETURNS:
    - cleaned_list: Python list that contains the phonemes as strings 
'''
def get_phoneme_list():
    # gets the name of the file, opens it, and reads the contents in
    phoneme_file_name = input("Enter file containing phonemenes: \n")
    phoneme_file = open(phoneme_file_name, "r")
    phonemes = phoneme_file.readlines()

    # closes the file since we extracted all the contents out of it
    phoneme_file.close()
    
    # goes through each of the phoneme and strips/"cleans" off the newline
    cleaned_list = []
    for phoneme in phonemes:
        phoneme_cleaned = phoneme.rstrip("\n")
        cleaned_list.append(phoneme_cleaned)
        
    return cleaned_list

def main():
    phoneme_list = get_phoneme_list()
    subject_name = input("Enter the name of the person's recordings (Folder Name): \n")
    normalized = input("Normalize the phonemes volume? (True / False): \n")
    pitch_shift = input("Pitch shift the words? (True / False) \n")
    pronunciation_dictionary = get_pronunciation_dictionary(subject_name, phoneme_list, normalized)
    create_artificial_data(subject_name, pronunciation_dictionary, pitch_shift)
    

main()

