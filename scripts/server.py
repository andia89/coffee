import socket
import sys
import threading
from time import sleep

matchfile = '/home/pi/coffee/scripts/stolen'

class Server():
	
    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('128.131.60.73', 10002)
        self.sock.bind(self.server_address)
        self.sock.listen(1)
        self.thread_server = threading.Thread(target=self.thread_server_worker)
        self.thread_server.wants_abort = False
        self.thread_server.start()

    def __del__(self):
        if self.thread_server.isAlive():
            self.thread_server.wants_abort = True
            self.thread_server.join()
            return
		
    def thread_server_worker(self):
        while not self.thread_server.wants_abort:
            connection, client_address = self.sock.accept()
            try:
                data = connection.recv(512).rstrip()
                if data=='match':
                    with open(matchfile, 'r') as mf:
                        response = mf.read()
                    sleep(.5)
                    connection.sendall(str(response))
                else:
                    break
            finally:
                connection.close()
        self.sock.close()

if __name__=="__main__":
    serv=Server()
    serv.start()
