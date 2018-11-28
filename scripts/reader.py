#!/usr/bin/env python
# -*- coding: utf8 -*-

from pirc522 import RFID
from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import threading
import time
import datetime
import sqlite3


def sql_insert(connection, coffeeid):
    date = datetime.datetime.now()
    dated = datetime.datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
    connection.execute('''INSERT INTO TICKS (DAT, COFFEEID) VALUES ("%s", %i)''' % (dated, coffeeid))
    connection.commit()


def get_counts():
    connection = sqlite3.connect(filename)
    offset_date, offset_count = connection.execute("SELECT * FROM COUNTER").fetchone()
    counts = connection.execute("SELECT COUNT(*) FROM TICKS WHERE '%s' < DAT" % (offset_date)).fetchone()[0]
    connection.close()
    counts = int(offset_count) - counts
    return counts


def write_stolenfile(val):
    with open(stolenfile, 'w')as stolenf:
        stolenf.write(val)


counterfile = '/home/pi/coffee/scripts/counter'
stolenfile = '/home/pi/coffee/scripts/stolen'
filename = "/home/pi/coffee/scripts/coffee.db"

price_coffee = 0.3

smiley = (0b00000, 0b01010, 0b01010, 0b00000,
          0b10001, 0b10001, 0b01110, 0b00000,)
neutral_smiley = (0b00000, 0b01010, 0b01010, 0b00000,
                  0b00000, 0b11111, 0b00000, 0b00000,)
sad_smiley = (0b00000, 0b01010, 0b01010, 0b00000,
              0b01110, 0b10001, 0b10001, 0b00000,)


class Reader():

    def __init__(self, log):
        self.grace_time = 25.
        self.grace_time_before = 8.
        self.app_log = log
        self.chip_detected = None
        
    def setup(self):
        self.MIFAREReader = RFID(pin_rst=36)
        self.lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=True)
        self.lcd.create_char(0, smiley)
        self.lcd.create_char(1, sad_smiley)
        self.lcd.create_char(2, neutral_smiley)
    
    def check_reader(self):
        error_cont = True
        while error_cont:
            self.chip_detected = None
            self.MIFAREReader.wait_for_tag()
            (error, TagType) = self.MIFAREReader.request()
            (error, uid) = self.MIFAREReader.anticoll()
            if not error:
                self.chip_detected = uid
                error_cont = False
        
    def main(self, match_value, blink_value, photo_value, cont_value):
        try:
            self.setup()
            write_stolenfile("0")
            match_value.value = 0
            blink_value.value = 0
            photo_value.value = 0
            start = 0
            offset_written = False
            match_flag = False
            drink_time = 0.0
            stolen_time = 0.0
            stolen = False
            t = threading.Thread(target = self.check_reader)
            t.start()
            while cont_value.value:
                time.sleep(0.1)
                match = match_value.value
                if not match_flag:
                    match_time = time.time()
                    match_flag = True
                if match: 
                    timenow = time.time()
                    if (abs(drink_time-timenow) > self.grace_time and abs(match_time-timenow) > self.grace_time_before) and not stolen:
                        stolen = True
                        self.app_log.critical('Someone stole coffee')
                        self.lcd.clear()
                        self.lcd.write_string('How about\n\r       paying?')
                        stolen_time = time.time()
                        write_stolenfile('1')
                        match_value.value = 1
                        photo_value.value = 1
                        blink_value.value = 1
                    elif abs(drink_time-timenow) <= self.grace_time:
                        write_stolenfile('0')
                        stolen = False
                        blink_value.value = 0
                        match_value.value = 0
                        photo_value.value = 0
                    if stolen:
                        if abs(stolen_time - timenow) > 20:
                            write_stolenfile('0')
                            blink_value.value = 0
                            match_value.value = 0
                            photo_value.value = 0
                            stolen = False
                            offset_count = get_counts()
                            self.lcd.clear()
                            self.lcd.write_string("Counter is: %s" % str(offset_count))
                else:
                    match_flag = False

                if self.chip_detected is not None:
                    offset_written = False
                    uid = ''.join((str(x) for x in self.chip_detected))
                    conn = sqlite3.connect(filename)
                    try:
                        name, firstname, coffeeid = conn.execute("SELECT NAME, FIRSTNAME, COFFEEID FROM COFFEE WHERE ID=%i AND ACTIVE=1" % (int(uid))).fetchone()
                    except Exception:
                        name = ""
                        firstname = ""
                        coffeeid = None
                    conn.close()
                    start = time.time()
                    timestr = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
                    if coffeeid:
                        conn = sqlite3.connect(filename)
                        if not firstname:
                            firstname = ""
                        sql_insert(conn, coffeeid)
                        try:
                            inp = conn.execute("SELECT SUM(MONEY) FROM INPUT WHERE COFFEEID=%i" % (coffeeid)).fetchone()[0]
                            counts = conn.execute("SELECT COUNT(*) FROM TICKS WHERE COFFEEID=%i" % (coffeeid)).fetchone()[0]
                            saldo = int(inp/price_coffee) - counts
                        except:
                            saldo = 0
                        conn.close()
                        drink_time = time.time()
                        stolen = False
                        write_stolenfile('0')
                        blink_value.value = 0
                        match_value.value = 0
                        photo_value.value = 0
                        if coffeeid == -1:
                            print "%s - Hello, enjoy your coffee!" % timestr
                            self.app_log.info("Hello guest, enjoy your coffee - ID: -1")
                            self.lcd.clear()
                            self.lcd.write_string('Hello, enjoy\n\ryour coffee!')
                        else:
                            print "%s - %s %s - Saldo: %i coffees" % (timestr, firstname, name, int(saldo))
                            self.app_log.info("%s %s - Saldo: %i coffees - ID: %i" % (firstname, name, int(saldo), coffeeid))
                            self.lcd.clear()
                            message1 = u"Hi %s,\n\r"%(firstname)
                            message2 = "Saldo: %i cfs "%(int(saldo))
                            self.lcd.write_string(message1 + message2)
                            if len(message2) <= self.lcd.lcd.cols:
                                if saldo > 0:
                                    self.lcd.write_string(unichr(0))
                                elif saldo == 0:
                                    self.lcd.write_string(unichr(2))
                                elif saldo < 0:
                                    self.lcd.write_string(unichr(1))
                        time.sleep(2)
                    else:
                        print "%s - %i - Please register your chip" %(timestr, int(uid))
                        self.app_log.warning("%i - Please register your chip"%(int(uid)))
                        self.lcd.clear()
                        self.lcd.write_string("Unknown\n\rPlease register")
                        time.sleep(2)
                    t = threading.Thread(target = self.check_reader)
                    t.start()
                end = time.time()
                if end-start > 5:
                    if not offset_written:
                        offset_count = get_counts()
                        self.lcd.clear()
                        self.lcd.write_string("Counter is: %s" % str(offset_count))
                        offset_written = True
        except Exception, e:
            print e
            self.app_log.exception("Exception in reader.py")
            self.app_log.exception(e)
            cont_value.value = False
        finally:
            GPIO.cleanup()
