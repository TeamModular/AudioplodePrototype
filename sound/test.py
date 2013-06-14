import sound
import thread
import time

test=sound.sound()

import fluidsynth
import numpy
import pyaudio
pa = pyaudio.PyAudio()
strm = pa.open(format = pyaudio.paInt16,channels = 2, rate = 44100,  output = True)

handles=[pa.open(format = pyaudio.paInt16,channels = 2, rate = 44100,  output = True) for i in xrange(29)]

for i in xrange(29):
	thread.start_new_thread(test.octave,(handles[i],))			
	time.sleep(1)

#test.base()
#test.high()
#test.octave()
print 'done'
time.sleep(5)
