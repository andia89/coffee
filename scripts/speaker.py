import wiringpi
import time
import multiprocessing

SoundPin = 13
message = "Federica..."
dotlength = 0.1
pause = dotlength

morseAlphabet ={
        "A" : ".-", "B" : "-...", "C" : "-.-.", "D" : "-..",
        "E" : ".", "F" : "..-.", "G" : "--.", "H" : "....",
        "I" : "..", "J" : ".---", "K" : "-.-", "L" : ".-..",
        "M" : "--", "N" : "-.", "O" : "---", "P" : ".--.",
        "Q" : "--.-", "R" : ".-.", "S" : "...", "T" : "-",
        "U" : "..-", "V" : "...-", "W" : ".--", "X" : "-..-",
        "Y" : "-.--", "Z" : "--..", " " : "/", '0': '-----',  
        '1': '.----', '2': '..---', '3': '...--', '4': '....-',
        '5': '.....', '6': '-....', '7': '--...', '8': '---..',
        '9': '----.', '.':'.-.-.-', ',':'--..--', ':':'---...',
        '?':'..--..', "'":'.----.', '-':'-....-', '/':'-..-.',
        '@': '.--.-.', '=':'-...-', '(':'-.--.', ')':'-.--.-',
        '+':'.-.-.', "!":'-.-.--'
        }



def encodeToMorse(message):
    encodedMessage = ""
    for char in message[:]:
        encodedMessage += morseAlphabet[char.upper()] + " "        
    return encodedMessage


class Buzzer:

    def __init__(self, log):
        self.log = log

    def setup(self):
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(SoundPin, 1)
        wiringpi.digitalWrite(SoundPin, 0)
        self.message = encodeToMorse(message)

    def main(self, stolen, overdue, cont):
        try:
            self.setup()
            wiringpi.digitalWrite(SoundPin, 0)
            while cont.value:
                if stolen.value:
                    for char in self.message:
                        if not stolen.value:
                            wiringpi.digitalWrite(SoundPin, 0)
                            break
                        if char == ".":
                            wiringpi.digitalWrite(SoundPin, 1)
                            time.sleep(dotlength)
                        elif char == "-":
                            wiringpi.digitalWrite(SoundPin, 1)
                            time.sleep(dotlength*3)
                        elif char == " ":
                            wiringpi.digitalWrite(SoundPin, 0)
                            time.sleep(dotlength*3)
                        else:
                            wiringpi.digitalWrite(SoundPin, 0)
                            time.sleep(dotlength*6)
                        wiringpi.digitalWrite(SoundPin, 0)
                        time.sleep(pause)
                    time.sleep(pause*5)
                else if overdue.value:
                    wiringpi.digitalWrite(SoundPin, 1)
                    time.sleep(10)
                    wiringpi.digitalWrite(SoundPin, 0)
                    overdue.value = 0
                else:
                    time.sleep(0.5)
        except Exception, e:
            print e
            self.log.exception("Error in speaker.py")
            self.log.exception(e)


if __name__ == "__main__":
    boolean = multiprocessing.Value('i', 1)
    stolen = multiprocessing.Value('i', 1)

    buzz = Buzzer(None)
    buzz.main(stolen, boolean)
