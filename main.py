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

'''struct parses the binary file, sys reads from command line'''
import struct, sys

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
track1 = MidiTrack()
track2 = MidiTrack()
track3 = MidiTrack()
track4 = MidiTrack()
track5 = MidiTrack()
track6 = MidiTrack()
track7 = MidiTrack()
track8 = MidiTrack()
midi.tracks.append(track1)
midi.tracks.append(track2)
midi.tracks.append(track3)
midi.tracks.append(track4)
midi.tracks.append(track5)
midi.tracks.append(track6)
midi.tracks.append(track7)
midi.tracks.append(track8)
track1.append(Message('program_change', program=88, channel=1, time=0))
track2.append(Message('program_change', program=89, channel=2, time=0))
track3.append(Message('program_change', program=90, channel=3, time=0))
track4.append(Message('program_change', program=91, channel=4, time=0))
track5.append(Message('program_change', program=92, channel=5, time=0))
track6.append(Message('program_change', program=93, channel=6, time=0))
track7.append(Message('program_change', program=94, channel=7, time=0))
track8.append(Message('program_change', program=95, channel=8, time=0))

'''
If a command line argument exists, use it as the name.
Otherwise, ask for input.
'''
if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    name = input("Please input a file: ")

'''Getting the data from the binary file'''
f = open(name, "rb")
data = f.read()
f.close()

'''Some counters, containers and constants'''
inputs = []
clock1, clock2, clock3, clock4, clock5, clock6, clock7, clock8 = 0, 0, 0, 0, 0, 0, 0, 0
clockStep = 16

'''A lookup table to the note value and weither or not it is active'''
notes = {0: [48, [False, False, False, False, False, False, False, False]],
         1: [50, [False, False, False, False, False, False, False, False]],
         2: [52, [False, False, False, False, False, False, False, False]],
         3: [55, [False, False, False, False, False, False, False, False]],
         4: [57, [False, False, False, False, False, False, False, False]],
         5: [60, [False, False, False, False, False, False, False, False]],
         6: [62, [False, False, False, False, False, False, False, False]],
         7: [64, [False, False, False, False, False, False, False, False]],
         8: [67, [False, False, False, False, False, False, False, False]],
         9: [69, [False, False, False, False, False, False, False, False]],
         10: [72, [False, False, False, False, False, False, False, False]],
         11: [74, [False, False, False, False, False, False, False, False]],
         12: [76, [False, False, False, False, False, False, False, False]],
         13: [79, [False, False, False, False, False, False, False, False]],
         14: [81, [False, False, False, False, False, False, False, False]],
         15: [84, [False, False, False, False, False, False, False, False]]}

'''Parsing the data into individual frames'''
inputs = struct.iter_unpack("cccccccccccccccc", data)

'''
For each frame:
Turn the binary data into a bit array for each controller
Set the first flag to true for each controller
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
    
    c1 = format(int(i[0].hex(), 16), "08b") + format(int(i[1].hex(), 16), "08b")
    c2 = format(int(i[2].hex(), 16), "08b") + format(int(i[3].hex(), 16), "08b")
    c3 = format(int(i[4].hex(), 16), "08b") + format(int(i[5].hex(), 16), "08b")
    c4 = format(int(i[6].hex(), 16), "08b") + format(int(i[7].hex(), 16), "08b")
    c5 = format(int(i[8].hex(), 16), "08b") + format(int(i[9].hex(), 16), "08b")
    c6 = format(int(i[10].hex(), 16), "08b") + format(int(i[11].hex(), 16), "08b")
    c7 = format(int(i[12].hex(), 16), "08b") + format(int(i[13].hex(), 16), "08b")
    c8 = format(int(i[14].hex(), 16), "08b") + format(int(i[15].hex(), 16), "08b")
    
    first1, first2, first3, first4, first5, first6, first7, first8 = True, True, True, True, True, True, True, True
    
    for key in notes.keys():

        '''Controller 1'''
        if c1[key] == "1":
            if notes[key][1][0] == False:
                if first1:
                    track1.append(Message('note_on', note=notes[key][0], velocity=64, channel=1, time=clock1))
                    first1 = False
                else:
                    track1.append(Message('note_on', note=notes[key][0], velocity=64, channel=1, time=0))
                notes[key][1][0] = True
                clock1 = 0
                
        elif c1[key] == "0":
            if notes[key][1][0] == True:
                if first1:
                    track1.append(Message('note_off', note=notes[key][0], velocity=64, channel=1, time=clock1))
                    first1 = False
                else:
                    track1.append(Message('note_off', note=notes[key][0], velocity=64, channel=1, time=0))
                notes[key][1][0] = False
                clock1 = 0

        '''Controller 2'''
        if c2[key] == "1":
            if notes[key][1][1] == False:
                if first2:
                    track2.append(Message('note_on', note=notes[key][0], velocity=64, channel=2, time=clock2))
                    first2 = False
                else:
                    track2.append(Message('note_on', note=notes[key][0], velocity=64, channel=2, time=0))
                notes[key][1][1] = True
                clock2 = 0
                
        elif c2[key] == "0":
            if notes[key][1][1] == True:
                if first2:
                    track2.append(Message('note_off', note=notes[key][0], velocity=64, channel=2, time=clock2))
                    first2 = False
                else:
                    track2.append(Message('note_off', note=notes[key][0], velocity=64, channel=2, time=0))
                notes[key][1][1] = False
                clock2 = 0

        '''Controller 3'''
        if c3[key] == "1":
            if notes[key][1][2] == False:
                if first3:
                    track3.append(Message('note_on', note=notes[key][0], velocity=64, channel=3, time=clock3))
                    first3 = False
                else:
                    track3.append(Message('note_on', note=notes[key][0], velocity=64, channel=3, time=0))
                notes[key][1][2] = True
                clock3 = 0
                
        elif c3[key] == "0":
            if notes[key][1][2] == True:
                if first3:
                    track3.append(Message('note_off', note=notes[key][0], velocity=64, channel=3, time=clock3))
                    first3 = False
                else:
                    track3.append(Message('note_off', note=notes[key][0], velocity=64, channel=3, time=0))
                notes[key][1][2] = False
                clock3 = 0

        '''Controller 4'''
        if c4[key] == "1":
            if notes[key][1][3] == False:
                if first4:
                    track4.append(Message('note_on', note=notes[key][0], velocity=64, channel=4, time=clock4))
                    first4 = False
                else:
                    track4.append(Message('note_on', note=notes[key][0], velocity=64, channel=4, time=0))
                notes[key][1][3] = True
                clock4 = 0
                
        elif c4[key] == "0":
            if notes[key][1][3] == True:
                if first4:
                    track4.append(Message('note_off', note=notes[key][0], velocity=64, channel=4, time=clock4))
                    first4 = False
                else:
                    track4.append(Message('note_off', note=notes[key][0], velocity=64, channel=4, time=0))
                notes[key][1][3] = False
                clock4 = 0

        '''Controller 5'''
        if c5[key] == "1":
            if notes[key][1][4] == False:
                if first5:
                    track5.append(Message('note_on', note=notes[key][0], velocity=64, channel=5, time=clock5))
                    first5 = False
                else:
                    track5.append(Message('note_on', note=notes[key][0], velocity=64, channel=5, time=0))
                notes[key][1][4] = True
                clock5 = 0
                
        elif c5[key] == "0":
            if notes[key][1][4] == True:
                if first5:
                    track5.append(Message('note_off', note=notes[key][0], velocity=64, channel=5, time=clock5))
                    first5 = False
                else:
                    track1.append(Message('note_off', note=notes[key][0], velocity=64, channel=5, time=0))
                notes[key][1][4] = False
                clock5 = 0

        '''Controller 6'''
        if c6[key] == "1":
            if notes[key][1][5] == False:
                if first6:
                    track6.append(Message('note_on', note=notes[key][0], velocity=64, channel=6, time=clock6))
                    first6 = False
                else:
                    track6.append(Message('note_on', note=notes[key][0], velocity=64, channel=6, time=0))
                notes[key][1][5] = True
                clock6 = 0
                
        elif c6[key] == "0":
            if notes[key][1][5] == True:
                if first6:
                    track6.append(Message('note_off', note=notes[key][0], velocity=64, channel=6, time=clock6))
                    first6 = False
                else:
                    track1.append(Message('note_off', note=notes[key][0], velocity=64, channel=6, time=0))
                notes[key][1][5] = False
                clock6 = 0

        '''Controller 7'''
        if c7[key] == "1":
            if notes[key][1][6] == False:
                if first7:
                    track7.append(Message('note_on', note=notes[key][0], velocity=64, channel=7, time=clock7))
                    first7 = False
                else:
                    track7.append(Message('note_on', note=notes[key][0], velocity=64, channel=7, time=0))
                notes[key][1][6] = True
                clock7 = 0
                
        elif c7[key] == "0":
            if notes[key][1][6] == True:
                if first7:
                    track7.append(Message('note_off', note=notes[key][0], velocity=64, channel=7, time=clock7))
                    first7 = False
                else:
                    track7.append(Message('note_off', note=notes[key][0], velocity=64, channel=7, time=0))
                notes[key][1][6] = False
                clock7 = 0

        '''Controller 8'''
        if c8[key] == "1":
            if notes[key][1][7] == False:
                if first8:
                    track8.append(Message('note_on', note=notes[key][0], velocity=64, channel=8, time=clock8))
                    first8 = False
                else:
                    track8.append(Message('note_on', note=notes[key][0], velocity=64, channel=8, time=0))
                notes[key][1][7] = True
                clock8 = 0
                
        elif c8[key] == "0":
            if notes[key][1][7] == True:
                if first8:
                    track8.append(Message('note_off', note=notes[key][0], velocity=64, channel=8, time=clock8))
                    first8 = False
                else:
                    track8.append(Message('note_off', note=notes[key][0], velocity=64, channel=8, time=0))
                notes[key][1][7] = False
                clock8 = 0
                

    clock1 += clockStep
    clock2 += clockStep
    clock3 += clockStep
    clock4 += clockStep
    clock5 += clockStep
    clock6 += clockStep
    clock7 += clockStep
    clock8 += clockStep

'''Output the midi with the same name.'''
midi.save(name + ".mid")
print("Done.")
