import multiprocessing
import time

filename = '/home/pi/coffee/scripts/trigger'

class Trigger:
    def __init__(self, log):
        self.log = log
        self.write_zero()
        
    def read_file(self):
        with open(filename, 'r') as f:
            val = int(f.read())
        return val
        
    def write_zero(self):
        with open(filename, 'w') as f:
            f.write('0')

    def main(self, match, cont):
        try:
            while cont.value:
                val = self.read_file()
                if val == 1:
                    match.value = 1
                    self.write_zero()
                time.sleep(0.5)
        except Exception, e:
            print e
            self.log.exception("Exception in trigger.py")
