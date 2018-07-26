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

'''This creates the lookup table for the notes, either from the command line or the default.'''
if len(sys.argv) > 1:
  f = open(sys.argv[1])
  notes = f.readLine().split(" ")
  for i in range(len(notes)):
    notes[i] = [int(notes[i]), False]
else:
  notes = [[48, False], [51, False], [53, False], [55, False], [58, False], [60, False], [63, False], [65, False],
           [67, False], [70, False], [72, False], [75, False], [77, False], [79, False], [82, False], [84, False]]
'''
This bit iterates through every possible combination of chords and
adds them to the midi file. This will be a very long file.
It formats the iteration of the loop as a 16-bit bitstring.
Then, for each bit in the string, it checks if the state of the
note associated with that bit should change.
If so, then it writes a midi event to the track, adding the delta time
if it is the first event this loop, or with no time if it is not.
'''

for chord in range(256):
  chord = format(chord, "08b")
  firstOn, firstOff = True, True
  for i in range(len(chord)):
    bit = chord[i]
    if bit == "1":
      if notes[i][1] == False:
        if firstOn == True:
          track.append(Message('note_on', note=notes[i][0], velocity=64, channel=1, time=120))
        else:
          track.append(Message('note_on', note=notes[i][0], velocity=64, channel=1, time=0))
        firstOn = False
        notes[i][1] = True
  for i in range(len(chord)):
    if notes[i][1] == True:
      if firstOff == True:
        track.append(Message('note_off', note=notes[i][0], velocity=64, channel=1, time=120))
      else:
        track.append(Message('note_off', note=notes[i][0], velocity=64, channel=1, time=0))
      firstOff = False
      notes[i][1] = False

'''Finally, we write the midi object to a midi file.'''
midi.save("allChords.mid")
print("Done.")
