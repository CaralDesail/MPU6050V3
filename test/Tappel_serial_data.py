import serial
import re
from statistics import mean
import Tserialpart


done1=False



while not done1 : # First Frame

    liste_acc_val=Tserialpart.ard_to_xyz_list()

    print(liste_acc_val)


