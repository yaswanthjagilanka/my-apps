#!/usr/bin/env python2

# Code for implementing the whole PROJECT in PYTHON:
import RPi.GPIO as GPIO
import time
import serial
import os
from array import *
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
count = 0
temp = []
beat = 0
temp2 = 0
tx = 0
# initiate Serial
ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
# Define GPIO to LCD mapping
LCD_RS = 40
LCD_E = 38
LCD_D4 = 36
LCD_D5 = 32
LCD_D6 = 26
LCD_D7 = 24
Heart_out = 22
# Define some device constants
LCD_WIDTH = 16  # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005


def main():

    # Main program block
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)  # Use BOARD PIN numbers
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT)  # RS
    GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
    GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
    GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
    GPIO.setup(LCD_D7, GPIO.OUT)  # DB7
    GPIO.setup(Heart_out, GPIO.IN)  # HEART BEAT


GPIO.setup(18, GPIO.IN)  # Reset


def lcd_init():

    # Initialise display
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(E_DELAY)


def lcd_byte(bits, mode):

    # Send byte to data pins
    # bits = data
    # mode = True for character
    # False for command
    GPIO.output(LCD_RS, mode)  # RS
    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)
    # Toggle 'Enable' pin
    lcd_toggle_enable()
    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)
    # Toggle 'Enable' pin
    lcd_toggle_enable()


def lcd_toggle_enable():

    # Toggle enable
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)


def lcd_string(message, line):

    # Send string to display
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()
    # Initialise display
    lcd_init()
    while True:
        ser.write("a")
        for k in range(0, 7):
            data = ser.read()
            if (data >= 0):
                temp.insert(k, data)
                temp1 = "".join(temp)
                list([temp.pop() for z in range(len(temp))])
                print temp1
                temp2 = float(temp1)
                temp2 = temp2-6
                print temp2
                temp1 = str(temp2)
                lcd_string("Temp-"+temp1, LCD_LINE_1)
                lcd_string("`C", LCD_LINE_1 + 11)
                time.sleep(1)
            if (GPIO.input(18) == 1):
                beat = 0
                lcd_string("Heart beat-"+str(beat), LCD_LINE_2)
            # lcd_byte(0x01,LCD_CMD)
            if (GPIO.input(22) == 1):
                for j in range(0, 301):
                    if (GPIO.input(22) == 1):
                        beat += 1
                        j += 1
                        lcd_string("Heart beat-"+str(beat), LCD_LINE_2)
                        lcd_string(str(j), LCD_LINE_1+14)
                        time.sleep(0.2)
                        f_beat = beat
                        beatstr = str(beat)
                        print beatstr
                        fromaddr = "pihealthmonitor@gmail.com"
                        toaddr = "8500374878@sms.textlocal.in"
                        msg = MIMEMultipart()
                        msg['From'] = fromaddr
                        msg['To'] = toaddr
                        msg['Subject'] = "SUBJECT"
                        42
                        body = "#%#YOUR HEART BEAT COUNT IS "+beatstr + \
                            " be careful and your temp is "+temp1+"'C ##"
                        msg.attach(MIMEText(body, 'plain'))
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(fromaddr, "pimonitorhealth")
                        text = msg.as_string()
                        server.sendmail(fromaddr, toaddr, text)
                        server.quit()
                        beat = 0
