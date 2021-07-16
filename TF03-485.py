# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import serial
import time

#if use half-auto, EN_485 = LOW is Receiver, EN_485 = HIGH is Send
MODE = 0 #mode = 0 is full-guto, mode = 1 is half-auto
if MODE == 1:
    EN_485 =  4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(EN_485,GPIO.OUT)
    GPIO.output(EN_485,GPIO.HIGH)

ser = serial.Serial("/dev/ttyS0",115200,timeout=0.01) #Set a read timeout value of 0.01S
#ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=0.01) # for Raspberry Pi ZERO/3B
#ser = serial.Serial("/dev/tty0", 115200, timeout=0.01)

ser.reset_input_buffer()

def read_data():
    while True:
        counter = ser.in_waiting # count the number of bytes of the serial port
        if counter > 8:
            bytes_serial = ser.read(9)
            ser.reset_input_buffer()

            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # this portion is for python3
                print("Printing python3 portion")            
                distance = bytes_serial[2] + bytes_serial[3]*256
                strength = bytes_serial[4] + bytes_serial[5]*256
                print("Distance:"+ str(distance))
                print("Strength:" + str(strength)+ "\n")
                ser.reset_output_buffer()

            if bytes_serial[0] == "Y" and bytes_serial[1] == "Y":
                distL = int(bytes_serial[2].encode("hex"), 16)
                distH = int(bytes_serial[3].encode("hex"), 16)
                stL = int(bytes_serial[4].encode("hex"), 16)
                stH = int(bytes_serial[5].encode("hex"), 16)
                distance = distL + distH*256
                strength = stL + stH*256
                print("Printing python2 portion")
                print("Distance:"+ str(distance))
                print("Strength:" + str(strength) + "\n")
                ser.reset_output_buffer()


if __name__ == "__main__":
    try:
        if ser.isOpen() == False:
            ser.open()
        print ("[INFO] Serial port: "+ str(ser.portstr))
        print("[INFO] You will continuously receive data, press Ctrl + C to exit")
        print("[INFO] This code works with Python2 and Python3 \n")
        time.sleep(5)
        read_data()
    except KeyboardInterrupt(): # ctrl + c in terminal.
        if ser != None:
            ser.close()
            print("program interrupted by the user")