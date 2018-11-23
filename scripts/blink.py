import RPi.GPIO as GPIO
import time

LedPin = 13

class Blink:

    def __init__(self, log):
        self.log = log

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(LedPin, GPIO.OUT)
        GPIO.output(LedPin, GPIO.LOW)

    def main(self, stolen, cont):
        try:
            self.setup()
            GPIO.output(LedPin, GPIO.LOW)
            while cont.value:
                if stolen.value:
                    GPIO.output(LedPin, GPIO.HIGH)  
                    time.sleep(0.5)
                    GPIO.output(LedPin, GPIO.LOW) 
                    time.sleep(0.5)
                else:
                    time.sleep(0.5)
        except Exception, e:
            print e
            self.log.exception("Exception in blink.py")
        finally:
            GPIO.cleanup()

