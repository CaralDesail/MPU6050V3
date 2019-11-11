"""In this module, will appear the com port and the bautrate
The principal purpose is to avoid to change in any file the port name when it changes"
"""
import serial

ser = serial.Serial('COM4')  # open serial port
ser.baudrate = 57600 #  don't works with any other values ie 9600