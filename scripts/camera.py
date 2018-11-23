import io
import time
import shutil
import threading
import os
import signal
import multiprocessing
import picamera


class Camera:

    def __init__(self, log):
        self.streamlist = [io.BytesIO() for l in range(50)]
        self.counter = 0
        self.continue_capture = True
        self.log = log
        self.dt = 1.
        
    def write_to_file(self, t):
        folder_name = '/home/pi/coffee/pictures/' + time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(t))
        secs = [i-len(self.streamlist)/2 for i in range(len(self.streamlist))]
        lt = [time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(t+i)) for i in secs]
        sl = self.streamlist[:]
        os.makedirs(folder_name)
        for i, stream in enumerate(sl):        
            stream.seek(0)
            with open(folder_name + '/' + lt[i] + '.jpeg', 'wb') as f:
                shutil.copyfileobj(stream, f)
            stream.flush()

    def main(self, take_photo, cont):
        try:
            self.camera = picamera.PiCamera()
            self.camera.start_preview()
            self.capture_thread = threading.Thread(target=self.capture)
            self.capture_thread.start()
            while cont.value:
                if take_photo.value:
                    t = time.time()
                    time.sleep(len(self.streamlist)/2*self.dt)
                    self.write_to_file(t)
                    take_photo.value = 0
                time.sleep(0.5)
            self.camera.stop_preview()
        except Exception, e:
            print e
            self.log.exception("Exception in camera.py")


    def capture(self):
        while self.continue_capture:
            stream = self.streamlist[self.counter]            
            stream.flush()
            stream.seek(0)
            self.camera.capture(stream, 'jpeg')
            self.counter += 1
            if self.counter >= len(self.streamlist):
                self.counter = 0
            time.sleep(self.dt)


if __name__ == "__main__":
    s = Camera(None)
    boolean = multiprocessing.Value('i', 1)
    match = multiprocessing.Value('i', 0)
    s.main(match, boolean)
            
