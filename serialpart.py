"""In this module, will appear the com port and the bautrate
The principal purpose is to avoid to change in any file the port name when it changes"
After, it contain a function to "format" the data with new arduino code and serial print
"""
import serial
import re

ser = serial.Serial('COM3')  # open serial port
ser.baudrate = 38400

cache_serial = str()

def simpleard_to_xyz_list(): # simple reading of arduino informations : the purpose is to return a x , y , z list

    # reading part
    info_serial_tr = ser.readline()  # basis reading from serial port

    #define a if condition that takes the previous serial infos is non object
    if info_serial_tr==None:
        global cache_serial
        info_serial_tr = cache_serial

    cache_serial=info_serial_tr
    liste_acc_val_temp = re.findall('([-0-9][0-9]+)',
                                    str(info_serial_tr))  # we simplify the sentence, and extract data in a list
    liste_acc_val = liste_acc_val_temp[0:3]

    print(info_serial_tr,cache_serial)

    if len(liste_acc_val) == 3 :
        return liste_acc_val
