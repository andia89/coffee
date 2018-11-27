import os
import time
import subprocess

filename = "/home/pi/coffee/scripts/cancel"

with open(filename, "w") as f:
    f.write("1")

ctr = 1
while ctr > 0:
    ctr = 0
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    for pid in pids:
        try:
            val = " ".join(open(os.path.join('/proc', pid, 'cmdline'), 'rb').read().split('\0'))
            if "coffee.py" in val:
                ctr += 1 
        except IOError: # proc has already terminated
            continue
    time.sleep(1)
    print("not stopped yet")
    
    

returncode = subprocess.call(["/usr/bin/sudo", "/home/pi/coffee_rfid"])    
