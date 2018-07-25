# Sound-of-TAS
Python script that turns binary files into midi files.

The Mido library is required, and the full list of dependencies is listed in dependences.txt.

The main.py script will turn any binary file given to it into a midi file. Currently the script supports <del>.r08</del> and .r16m file formats. If the file does not have one of the listed extensions, then it will ask you which format you wish to use. It will then ask if you wish to use a specific note lookup table or to just use the default. A note lookup table is just sixteen (16) integers seperated by spaces. These numbers must be associable with a midi note. The default table is an extension of the C Major pentatonic scale. Both the file path and the table path can be passed as command line argument to speed up the process. It will then spit out a midi file with the same name as the input.

I have tried to make everything python2 compatible. If you encounter an error, please put an issue in and I will try to fix it.
