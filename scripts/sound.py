import pyaudio
import time
import numpy
import scipy.io
import threading
import socket
import sys
import multiprocessing
import peakutils
import sqlite3
import pickle

RATE = 44100
FPB = 441*3
len_array = 103635
trainingfile = '/home/pi/coffee/scripts/training.db'

class Sound:

    def __init__(self, log):
        self.p = pyaudio.PyAudio()
        self.coffee_time = 0.0
        self.appended_data = numpy.zeros(len_array)
        self.sound_array = None
        self.dummy_array = self.appended_data.copy()
        self.ctr = 0
        self.previous_sample = numpy.array([0,0,0])
        self.ctr_end = 2000
        self.thres = 1.
        self.corr = 0.
        self.log = log
        self.training = False
        self.recorded_data = numpy.zeros((self.ctr_end+1)*FPB)
        try:
            with open('classifier.pkl', 'rb') as f:
                    self.mlp = pickle.load(f)
            self.classifier = True
        except:
            self.classifier = False

    def stop_stream(self):
        self.stream.close()
        self.p.terminate()

    def main(self, match, cont):
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=RATE, input=True, frames_per_buffer=FPB, stream_callback=self.global_callback)
        self.stream.start_stream()
        try:
            self.match = match
            while cont.value:
                if self.stream.is_active():
                    time.sleep(0.5)
                else:
                    self.log.exception("Sound stream stopped")
                    self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=RATE, input=True, frames_per_buffer=FPB, stream_callback=self.global_callback)
                    self.stream.start_stream()
                    time.sleep(0.5)

        except Exception, e:
            print e
            if self.log:
                self.log.exception("Exception in sound.py")
                self.log.exception(e)
        finally:
            self.stream.stop_stream()

    def record_callback(self, in_data, frame_count, time_info, flag):
         audio_data = numpy.fromstring(in_data, dtype=numpy.float64)
         self.recorded_data[self.ctr*FPB:(self.ctr+1)*FPB] = audio_data
         if self.ctr == self.ctr_end:
             self.ctr = 0
             return (audio_data, pyaudio.paAbort)
         else:
             self.ctr += 1
             return (audio_data, pyaudio.paContinue)

    def global_callback(self, in_data, frame_count, time_info, flag):
        try: 
            audio_data = numpy.fromstring(in_data, dtype=numpy.float32)
            if numpy.array_equal(audio_data[-3:], self.previous_sample):
                self.log.exception("Seems the audio stream stopped")
            self.appended_data = numpy.roll(self.appended_data, -FPB)
            self.appended_data[-FPB:] = audio_data
            if numpy.any(abs(self.appended_data[20000:35000]) >= self.thres) and abs(self.coffee_time-time.time()) > 10:
                self.sound_arr = self.appended_data.copy()
                if self.classifier:
                    if self.mlp.predict(abs(self.sound_arr).reshape(1, -1)):
                        self.match.value = 1
                if self.training:
                    dated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))                
                    conn = sqlite3.connect(trainingfile)
                    conn.execute('INSERT INTO STOLEN (DAT, STOLENARR) VALUES (?, ?)', (dated, sqlite3.Binary(self.sound_arr)))
                    conn.commit()
                    conn.close()
                self.coffee_time = time.time()
            self.previous_sample = audio_data[-3:].copy()    
        except Exception, e:
            print e
            if self.log:
                self.log.exception("Exception in sound.py")
                self.log.exception(e)
        return (audio_data, pyaudio.paContinue)

if __name__ == "__main__":
    s = Sound(None)
    s.training = False
    boolean = multiprocessing.Value('i', 1)
    match = multiprocessing.Value('i', 0)
    s.main(match, boolean)


