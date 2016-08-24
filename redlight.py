import pigpio

pi = pigpio.pi()
pi.set_PWM_dutycycle(PIN, BRIGHTNESS)

PIN = 24
BRIGHTNESS = 128

pi.stop()
