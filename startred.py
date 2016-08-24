import pigpio
pi = pigpio.pi()
pi.set_PWM_dutycycle(24, 128)
def setLights(pin, brightness):
	realBrightness = int(int(brightness) * (float(bright) / 255.0))
	pi.set_PWM_dutycycle(pin, realBrightness)
def getCh():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	
	try:
		tty.setraw(fd)
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		
	return ch

def getCh():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	
	try:
		tty.setraw(fd)
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		
	return ch


def checkKey():
	global bright
	global brightChanged
	global state
	global abort
	
	while True:
		c = getCh()
		
		if c == '+' and bright < 255 and not brightChanged:
			brightChanged = True
			time.sleep(0.01)
			brightChanged = False
			
			bright = bright + 1
			print ("Current brightness: %d" % bright)
			
		if c == '-' and bright > 0 and not brightChanged:
			brightChanged = True
			time.sleep(0.01)
			brightChanged = False
			
			bright = bright - 1
			print ("Current brightness: %d" % bright)
			
		if c == 'p' and state:
			state = False
			print ("Pausing...")
			
			time.sleep(0.1)
			
			setLights(RED_PIN, 0)
			setLights(GREEN_PIN, 0)
			setLights(BLUE_PIN, 0)
			
		if c == 'r' and not state:
			state = True
			print ("Resuming...")
			
		if c == 'c' and not abort:
			abort = True
			break

start_new_thread(checkKey, ())

setLights(24, r)
pi.stop()
