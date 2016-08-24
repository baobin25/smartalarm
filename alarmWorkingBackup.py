import threading
import time, json, datetime
import os
import sys
import tty
from thread import start_new_thread
import pigpio
from dateutil import parser
from ledstrip_bootstrap import *


seconds_per_minute  = 60
seconds_per_day  = seconds_per_minute*60*24
minutes_per_day  = seconds_per_day / 60 
text ='Ring Ring'

class Alarm(threading.Thread):
    __alarmTriggered = False
    __logging = None

    def __init__(self, timeOfDay, daysOfWeek, wakeUpMinutes=30, graceMinutes=10, delay=10):
        super(Alarm, self).__init__()
        
        self.timeOfDay = timeOfDay
        self.daysOfWeek = daysOfWeek
        self.delay = delay
        self.wakeUpMinutes = float(wakeUpMinutes)
        self.graceMinutes = graceMinutes
        self.setDaemon(True)
        self.led = led
        self.lock = threading.Lock()
        self.__isFinished = False
	self.__alarmTriggered = False
	__logging = None	

    def __str__(self):
        return str(self.dump())
    
    def  getLight(self, deltaMinutes):
        """
        deltaMinutes: number of minutes before alarm time
        generate r,g,b values 
        """
        if minutes_per_day - deltaMinutes < self.graceMinutes: return Color(255.0, 255.0, 255.0 , 1.0)
        if deltaMinutes > self.wakeUpMinutes: return None 
        level = 1.0 -   deltaMinutes / self.wakeUpMinutes
        red, green, blue = 255.0, 0.0, 255.0 * level 
        print(red,green, blue, self.wakeUpMinutes, deltaMinutes, level)
        return  Color(red,green,blue, level)
        
    def run(self):
        while True:
            time.sleep(self.delay)
            with self.lock: 
                if self.__isFinished: break
            self.tick()

    def tick(self):
       # currentTime = time.strftime('%H:%M')
        #if (currentTime == self.timeOfDay and self.__alarmTriggered == False):
        #	self.__logging.info('Wakeup time ' + self.timeOfDay + ' reached. Ring Ring! :-)')
        #	self.__alarmTriggered = True
        #	self.start()


        now = datetime.datetime.now()
#	if datetime.time == self.timeOfDay:
#		os.system("python alarmpi/sound_the_alarmtest.py")

        if not now.weekday() in self.daysOfWeek: return 
	delta =  self.timeOfDay - now 
        deltaMinutes = (delta.seconds  % seconds_per_day) / seconds_per_minute
        light = self.getLight(deltaMinutes)

	if deltaMinutes == 0:
		abort = False
		pi = pigpio.pi()
		if abort == False:
			pi.set_PWM_dutycycle(20, 255)
		time.sleep(60)
                os.system("python alarmpi/sound_the_alarmtest.py")
		abort = True
#	if deltaMinutes < 0.05 and deltaMinutes >= 0:
		
		if abort == True:
		#	time.sleep(6)
		#	pi.set_PWM_dutycycle(17, 0)
		#	pi.stop
			pi.set_PWM_dutycycle(20, 0)
		
			time.sleep(0.5)
	
			pi.stop()  
        #print(now, "setting light", str(light))
        if light is not None: self.setLight(light)

    def setLight(self, color):
        self.led.fill(color)
        self.led.update()

#    def startSound(self):
#    	os.system ("python alarmpi/sound_the_alarmtest.py")	
	

    def close(self):
        with self.lock:
            self.__isFinished = True

    def dump(self): 
        d = {
                "time": self.timeOfDay.isoformat(),
                "weekdays": self.daysOfWeek,
                "delay": self.delay,
                "grace": self.graceMinutes,
                "wakeUpMinutes": self.wakeUpMinutes} 
        return json.dumps(d)

    def toFile(self, filename):
        with open(filename, "w") as f:
            f.write(self.dump())

    @staticmethod 
    def loads(s): 
        d = json.loads(s)
        return Alarm(parser.parse(d["time"]),
                d["weekdays"],
                d["wakeUpMinutes"],
                d["grace"],
                d["delay"])

    @staticmethod
    def fromFile(filename):
        with open(filename, "r") as f:
            return Alarm.loads(
                    reduce(lambda a,b: a+b, f.readlines()))
#    def __loop(self):
#	currentTime = time.strftime('%H:%M')
#	if (currentTime == datetime.datetime.now() and self.__alarmTriggered == False):
#		self.__logging.info('Wakeup time ' + self.timeOfDay + ' reached. Ring Ring! :-)' 
#		print('Ring Ring')
#		self.__alarmTriggered = True
#		self.start()

#    def start(self):
#	os.system("python alarmpi/sound_the_alarmtest.py")

if __name__ == "__main__":
    state = Alarm(datetime.datetime.now(), [0,1,2,3])
    filename = "alarm.state.json"
    state.toFile(filename)
    state2 = Alarm.fromFile(filename)
    print("state2", state2.dump())
