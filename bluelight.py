import pigpio
PIN = 24
def on():
	pi.set_PWM_dutycycle(24, 128)

def off():
	pi.set_PWM_dutycycle(24, 0)

def run():
	print("Light up 60 seconds")
	off()


pi = pigpio.pi()


pi.stop()
