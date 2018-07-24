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

'''struct parses the binary file, sys rads from command line'''
import struct, sys

'''Mido facilitates the creation of the midi file'''
from mido import Message, MidiFile, MidiTrack

'''
This is all of the overhead for the midi file creation.
The midi object itself and the track for the notes.
I also set the instrument to 89. Counting is hard.
'''
midi = MidiFile()
track = MidiTrack()
midi.tracks.append(track)
track.append(Message('program_change', program=88, time=0))

'''
If a command line argument exists, use it as the name.
Otherwise, ask for input.
'''
if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    name = input("Please input a file: ")

'''Getting the data fromthe binary file'''
f = open(name, "rb")
data = f.read()
f.close()

'''Some counters, containers and constants'''
inputs = []
clock = 0
clockStep = 16

'''A lookup table to the note value and weither or not it is active'''
notes = {0: [48, False],
         1: [50, False],
         2: [52, False],
         3: [55, False],
         4: [57, False],
         5: [60, False],
         6: [62, False],
         7: [64, False],
         8: [67, False],
         9: [69, False],
         10: [72, False],
         11: [74, False],
         12: [76, False],
         13: [79, False],
         14: [81, False],
         15: [84, False]}

'''Parsing the data into individual frames'''
inputs = struct.iter_unpack("cccccccccccccccc", data)

'''
For each frame:
Turn the binary data into a bit array
Set the first flag to true
Check each bit for it's state
Check each note to see if it should change state
If it is the first note to change this frame:
    make sure the time attribute equals the clock
    otherwise time should always be 0
    Also, the clock is reset on any state change
Then, iterate the clock by the clock step

Since time is the delta since the last event, it will
always be very small unless there is a long silence.
'''
for i in inputs:
    
    latch = format(int(i[0].hex(), 16), "08b") + format(int(i[1].hex(), 16), "08b")
    first = True
    for key in notes.keys():
        if latch[key] == "1":
            if notes[key][1] == False:
                if first:
                    track.append(Message('note_on', note=notes[key][0], velocity=64, time=clock))
                    first = False
                else:
                    track.append(Message('note_on', note=notes[key][0], velocity=64, time=0))
                notes[key][1] = True
                clock = 0
                
        else:
            if notes[key][1] == True:
                if first:
                    track.append(Message('note_off', note=notes[key][0], velocity=64, time=clock))
                    first = False
                else:
                    track.append(Message('note_off', note=notes[key][0], velocity=64, time=0))
                notes[key][1] = False
                clock = 0

    clock += clockStep

'''Output the midi with the same name.'''
midi.save(name + ".mid")
print("Done.")

    
    
