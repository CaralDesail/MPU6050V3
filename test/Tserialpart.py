"""In this module, will appear the com port and the bautrate
The principal purpose is to avoid to change in any file the port name when it changes"
After, it contain a function to "format" the data with new arduino code and serial print
"""
import serial
import re

ser = serial.Serial('COM6')  # open serial port
ser.baudrate = 57600 #  don't works with any other values ie 9600



def simpleard_to_xyz_list(): # simple reading of arduino informations from
    # reading part
    info_serial_tr=ser.readline() # basis reading from serial port
    liste_acc_val= re.findall("(.[0-9]+)",str(info_serial_tr)) # we simplify the sentence, and extract data in a list

    return liste_acc_val
