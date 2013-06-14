import time
import numpy
import pyaudio
import fluidsynth
import thread

class sound:
	def __init__(self):
		"""
		Creates the handles and initalises
		fluidsynth soundbank
		calls _genTunes to generate the sounds
		"""
		
		pa = pyaudio.PyAudio()
		self._strm = pa.open(format = pyaudio.paInt16,channels = 2, rate = 44100,  output = True)
		
		self._fl = fluidsynth.Synth()
		# Initial silence is 1 second
		sfid = self._fl.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
		self._fl.program_select(0, sfid, 0, 0)
		
		self._genTunes()
				
		self._handles=[pa.open(format = pyaudio.paInt16,channels = 2, rate = 44100,  output = True) for handles in xrange(8)] #generate 8 handles to use

	def _genTunes(self):
		"""
		Fudging audio creation for now by just having 
		sounds made that all belong to
		one private list
		"""
		self._tunes=[]
		
		s=[]
		s = numpy.append(s, self._fl.get_samples(int(44100 * 0.1)))
		self._fl.noteon(0, 60, 120)
		s = numpy.append(s, self._fl.get_samples(int(44100 * 0.3)))
		self._fl.noteoff(0, 60)
		s = numpy.append(s, self._fl.get_samples(int(44100 * 0.1)))
		self._tunes.append(fluidsynth.raw_audio_string(s))

		s=[]
		s = numpy.append(s, self._fl.get_samples(int(44100 * 0.1)))
		self._fl.noteon(0, 67, 120)
		s = numpy.append(s, self._fl.get_samples(int(44100 * 0.3)))
		self._fl.noteoff(0, 67)
		s = numpy.append(s, self._fl.get_samples(int(44100 * 0.1)))
		self._tunes.append(fluidsynth.raw_audio_string(s))

		s=[]
		s = numpy.append(s, self._fl.get_samples(int(44100 * 0.1)))
		self._fl.noteon(0, 76, 120)
		s = numpy.append(s, self._fl.get_samples(int(44100 * 0.3)))
		self._fl.noteoff(0, 76)
		s = numpy.append(s, self._fl.get_samples(int(44100 * 0.1)))
		self._tunes.append(fluidsynth.raw_audio_string(s))

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
		self._tunes.append(fluidsynth.raw_audio_string(s))
		
		return
		
	def play(self,index):
		"""
		Given an integer index
		will play the corresponding sound
		"""
		assert type(index)==int
		assert index<len(self._tunes), "Trying to access unavailable tune. Make more Tunez"
		stream=self._handles.pop(0)	#pop handle from front

		thread.start_new_thread(stream.write,(self._tunes[index],) )
	
		self._handles.append(stream) #push at end
	
