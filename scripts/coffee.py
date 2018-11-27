#!/usr/bin/env python
# -*- coding: utf8 -*-


import signal
import time
import socket
import sys
import logging
import logging.handlers
import multiprocessing
#import blink
import sound
import camera
import reader
import speaker
import cancel
import trigger

def get_lock(process_name):
    global lock_socket_coffee
    lock_socket_coffee = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        lock_socket_coffee.bind('\0' + process_name)
        print "I got the lock"
        return False
    except socket.error:
        return True


if get_lock('coffee'):
    sys.exit()


def end_read(signal, frame):
    cont_value.value = False


signal.signal(signal.SIGINT, end_read)
signal.signal(signal.SIGTERM, end_read)


logfile = '/home/pi/coffee/scripts/coffeelog.log'
my_handler = logging.handlers.RotatingFileHandler(logfile, mode='a', maxBytes=5*1024*1024,
                                         backupCount=2, encoding=None, delay=0)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
my_handler.setFormatter(formatter)
app_log = logging.getLogger('root')
app_log.addHandler(my_handler)
app_log.setLevel(logging.INFO)


match_value = multiprocessing.Value('i', 0)
blink_value = multiprocessing.Value('i', 0)
photo_value = multiprocessing.Value('i', 0)
cont_value = multiprocessing.Value('i', 1)

cancel.reset()

use_soundcard = True
if use_soundcard:
    soundcard = True
    try:
        soundrec = sound.Sound(app_log)
    except:
        app_log.critical('Soundcard not initialized')
        soundcard = False
else:
    soundcard = False
cam = camera.Camera(app_log)
#blinker = blink.Blink(app_log)
speaker = speaker.Buzzer(app_log)
reader = reader.Reader(app_log)
trigger = trigger.Trigger(app_log)

use_cam = True


tmain = multiprocessing.Process(target=reader.main, name='reading', args=(match_value, blink_value, photo_value, cont_value))
if soundcard:
    tsound = multiprocessing.Process(target=soundrec.main, name='sound', args=(match_value, cont_value))
tcamera = multiprocessing.Process(target=cam.main, name='camera', args=(photo_value, cont_value))
#tblink = multiprocessing.Process(target=blinker.main, name='blinker', args=(blink_value, cont_value))
tspeaker = multiprocessing.Process(target=speaker.main, name='speaker', args=(blink_value, cont_value))
ttrigger = multiprocessing.Process(target=trigger.main, name='trigger', args=(match_value, cont_value))

if soundcard:
    tsound.start()
#tblink.start()
tspeaker.start()
ttrigger.start()
if use_cam:
    tcamera.start()
tmain.start()

while tmain.is_alive():
    cancel.cancel(cont_value)
    time.sleep(0.5)

cont_value.value = 0
