'''
Notes:        Dotted:
Whole:   1920 ticks  2880 ticks
Half:    960  ticks  1440 ticks
Quarter: 480  ticks  720  ticks
Eighth:  240  ticks  360  ticks
16th:    120  ticks  180  ticks
32th:    60   ticks  90   ticks
64th:    30   ticks  45   ticks
'''

'''sys reads from command line'''
import sys

'''Mido facilitates the creation of the midi file'''
from mido import Message, MidiFile, MidiTrack

'''python2 compatibility'''
from builtins import input
from builtins import range

'''
This is all of the overhead for the midi file creation.
The midi object itself and the tracks for the notes.
I also set the instrument to 89. Counting is hard.
'''
midi = MidiFile()
track = MidiTrack()
midi.tracks.append(track)
track.append(Message('program_change', program=88, channel=1, time=0))

