"""This script that will only call the reading and the functions of serialpart"""

import serialpart
import time


done1=False



while not done1 : # First Frame

    liste_acc_val=serialpart.simpleard_to_xyz_list()
    time.sleep(0.01)

    print(liste_acc_val)
