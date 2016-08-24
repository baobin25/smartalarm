#!/usr/bin/python
###### CONFIGURE THIS ######

# The Pins. Use Broadcom numbers.
RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24

# Number of color changes per step (more is faster, less is slower).
# You also can use 0.X floats.
STEPS     = 1

###### END ######




import os
import sys
import termios
import tty
import pigpio
import time
import alarm
from thread import start_new_thread

bright = 255
r = 255.0
g = 0.0
b = 0.0

pi = pigpio.pi()

def setLights(pin, brightness):
	realBrightness = int(int(brightness) * (float(bright) / 255.0))
	pi.set_PWM_dutycycle(pin, realBrightness)

setLights(RED_PIN, r)
setLights(GREEN_PIN, g)
setLights(BLUE_PIN, b)

def CheckKey():
	global abort
	if now == time + 60:
		abort = True

while abort == False:
	if state and not brightChanged:
		if r == 255 and b == 0 and g < 255:
			g = updateColor(g, STEPS)
			setLights(GREEN_PIN, g)
		
		elif g == 255 and b == 0 and r > 0:
			r = updateColor(r, -STEPS)
			setLights(RED_PIN, r)
		
		elif r == 0 and g == 255 and b < 255:
			b = updateColor(b, STEPS)
			setLights(BLUE_PIN, b)
		
		elif r == 0 and b == 255 and g > 0:
			g = updateColor(g, -STEPS)
			setLights(GREEN_PIN, g)
		
		elif g == 0 and b == 255 and r < 255:
			r = updateColor(r, STEPS)
			setLights(RED_PIN, r)
		
		elif r == 255 and g == 0 and b > 0:
			b = updateColor(b, -STEPS)
			setLights(BLUE_PIN, b)
	
print ("Aborting...")

setLights(RED_PIN, 0)
setLights(GREEN_PIN, 0)
setLights(BLUE_PIN, 0)

time.sleep(0.5)

pi.stop()
