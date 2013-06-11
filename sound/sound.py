import time
import numpy
import pyaudio
import fluidsynth

class sound:
	def __init__(self):

		pa = pyaudio.PyAudio()
		self._strm = pa.open(format = pyaudio.paInt16,channels = 2, rate = 44100,  output = True)
		
		self._fl = fluidsynth.Synth()
		# Initial silence is 1 second
		sfid = self._fl.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
		self._fl.program_select(0, sfid, 0, 0)
	
		self.gen()
		self.genHigh()
		self.genOct()
		##fl.delete()

	def gen(self):
		s=[]
		s = numpy.append(s, self._fl.get_samples(int(44100 * 0.1)))

		self._fl.noteon(0, 60, 120)
		#self._fl.noteon(0, 67, 120)
		#self._fl.noteon(0, 76, 120)
		
		s = numpy.append(s, self._fl.get_samples(int(44100 * 0.3)))
		self._fl.noteoff(0, 60)
		#self._fl.noteoff(0, 67)
		#self._fl.noteoff(0, 76)
	
		s = numpy.append(s, self._fl.get_samples(int(44100 * 0.1)))

		self._samps = fluidsynth.raw_audio_string(s)
		

	def genHigh(self):
		s=[]
		s = numpy.append(s, self._fl.get_samples(int(44100 * 0.1)))

		#self._fl.noteon(0, 60, 120)
		#self._fl.noteon(0, 67, 120)
		self._fl.noteon(0, 76, 120)
		
		s = numpy.append(s, self._fl.get_samples(int(44100 * 0.3)))
		#self._fl.noteoff(0, 55)
		#self._fl.noteoff(0, 67)
		self._fl.noteoff(0, 76)
		
		s = numpy.append(s, self._fl.get_samples(int(44100 * 0.1)))

		self._sampsHigh = fluidsynth.raw_audio_string(s)
	
	def genOct(self):
		s=[]
		s = numpy.append(s, self._fl.get_samples(int(44100 * 0.1)))
		for i in xrange(0,32,4):
			self._fl.noteon(0, 60+i, 120)
			s = numpy.append(s, self._fl.get_samples(int(44100 * 0.2)))
			self._fl.noteoff(0, i)
		for i in xrange(32,0,-4):
			self._fl.noteon(0, 60+i, 120)
			s = numpy.append(s, self._fl.get_samples(int(44100 * 0.2)))
			self._fl.noteoff(0, i)
			
		self._sampsOct = fluidsynth.raw_audio_string(s)	
	
	def base(self):
		self._strm.write(self._samps)
		
	def high(self):
		self._strm.write(self._sampsHigh)
		
	def octave(self):
		self._strm.write(self._sampsOct)
