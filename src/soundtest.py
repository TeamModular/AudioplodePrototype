import sound
#import thread
import time

test=sound.sound()

print 'done'

#quick chord test
test.play(0)
test.play(1)
test.play(2)

time.sleep(0.5)

#trying to break it by running too many threads
[test.play(2) for i in xrange(3)]

time.sleep(0.4)

#scale test
test.play(3)

time.sleep(3.5)

