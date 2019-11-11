import serial
import re
from statistics import mean
from random import *
import pygame
import datetime

pygame.init()  # intialisation of pygame
h_screen = 800  # definition of the screen
w_screen = 1280
screen = pygame.display.set_mode((w_screen, h_screen))  # display
done = False  # basis state of while
rectScreen = screen.get_rect()

backgr=pygame.image.load("ressources/Cartoon_Forest_BG_01.png").convert_alpha()
backgr = pygame.transform.scale(backgr, (w_screen, h_screen))


basketp=pygame.image.load("ressources/cesta.png").convert_alpha()
basketp = pygame.transform.scale(basketp, (60, 60))

nuttp=pygame.image.load("ressources/noisette.png").convert_alpha()
nuttp = pygame.transform.scale(nuttp, (20, 20))

sq_d_1frame=pygame.image.load("ressources/sq_d_1.png").convert_alpha()
sq_d_2frame=pygame.image.load("ressources/sq_d_2.png").convert_alpha()
sq_g_1frame=pygame.image.load("ressources/sq_g_1.png").convert_alpha()
sq_g_2frame=pygame.image.load("ressources/sq_g_2.png").convert_alpha()

x = int(100)
y = int(100)

""" the two following lines are about the dictionnary of projectiles called "objects" and goes from top to down"""
objectnumber = int(1)
dico = {}

""" about the MPU6050 fonctionnement"""
from serialpart import * #will import serialpart.py (with port name and baudrate)
num_val_mean = 10  # value of softener function
nb_of_px = 10  # speed of the controlled object (in px/while )
diff_factor = 1.0  # a factor that will change the values of nmin/nmax (used to change difficulty)

clock = pygame.time.Clock()
with open("ac_user", "r") as myuser:  # put it into a calibration_vars
    ac_us = myuser.read()
fenetre = pygame.display.set_mode((w_screen, h_screen))
police = pygame.font.Font(None, 72)  # size of the font
score_count=int(0)

xp = int(10)
yp = int(10)

n_m = int(0)  # meaned position of mpu on selected axis

color1 = (0, 128, 255)  # two differents colors that will be used. Or not.
color2 = (128, 255, 0)

list_to_meanX = []  # create a list in wich we'll put "num_val_mean" values before meaning it.
list_to_meanY = []  # the same with y

"""These two lines are used to "heat" the program, or more seriously to avoid launch errors 
(incomplete signals at the beginning)"""
print(ser.readline())
print(ser.readline())

with open("Calibration1D.txt", "r") as mycalfile:  # put it into a calibration_vars
    text_of_cal = mycalfile.read()
    list_of_cal1D = text_of_cal.split()

axis = int(list_of_cal1D[0])  # axis will be 0 if x, 1 if y
basis_value = int(list_of_cal1D[1])  # the value on axis of neutral articulation position
nmin = int(list_of_cal1D[2]) * diff_factor  # minimum recorded value time difficultyfactor
nmax = int(list_of_cal1D[3]) * diff_factor  # maximum recorded value time difficultyfactor


class Lanceur(pygame.sprite.Sprite):  # Creation of Launcher objet that will cruise the top of the screen
    def __init__(self, taille, distancex, distancey):
        self.taille = taille
        self.distancex = distancex
        self.distancey = distancey
        self.but = int(0)  # that remember if the object has gone on the extrems (in order to give the orientation)

    def afficher(self):

        if (int(self.distancex/10))%2==0:
            if self.but == 0:
                screen.blit(sq_d_1frame, (self.distancex-40, self.distancey - 40)) # we ajust the x position of sprite to avoid
                # the sensation that the squiell poes nuts and y position for conflict with score
            if self.but == 1:
                screen.blit(sq_g_1frame, (self.distancex, self.distancey - 40))
        else :
            if self.but == 0:
                screen.blit(sq_d_2frame, (self.distancex-40, self.distancey - 40))
            if self.but == 1:
                screen.blit(sq_g_2frame, (self.distancex, self.distancey - 40))

    def move(self, x):  # that will alternate between go right and go left

        if self.distancex >= w_screen - (self.taille / 2):
            self.but = 1
        if self.distancex <= 0:
            self.but = 0

        if self.but == 0:
            self.distancex = self.distancex + x
        if self.but == 1:
            self.distancex = self.distancex - x



class ObjetsLances(pygame.sprite.Sprite):  # about projectiles
    def __init__(self, distancex, distancey):
        pygame.sprite.Sprite.__init__(self)
        self.distancex = distancex
        self.distancey = distancey
        self.speedofprojectile = 2
        self.collid = 0

    def afficher(self):
        if self.collid==0:
             screen.blit(nuttp, (self.distancex, self.distancey))

    def move(self):  # that will alternate between go right and go left
        if self.distancey < h_screen-5:
            self.distancey = self.distancey + self.speedofprojectile

    def collide(self):
        if self.distancey == h_screen*0.93 and self.distancex > xp and self.distancex < xp+60:
            self.collid = 1
            global score_count
            score_count += 1



lanceur = Lanceur(20, 50, 50)

while not done:  # main loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("scores.txt", "r+") as myscorefile:  # put it into a scores with date
                text_rep = myscorefile.read()
                strsc = str("\n") + str(ac_us) + str(" ")+ str("CatchyP")+ str(" ") +str(datetime.datetime.now().day) + str('-') + str(datetime.datetime.now().month)\
                           + str('-') + str(datetime.datetime.now().year) + str(" ")+ str(datetime.datetime.now().hour)\
                           + str(':') + str(datetime.datetime.now().minute)\
                           + str(" ") + str(score_count)
                myscorefile.write(strsc)
            done = True

    # reading part
    info_serial_tr = ser.readline()  # basis reading from serial port
    liste_acc_val = re.findall("(.[0-9]+)", str(info_serial_tr))  # we simplify the sentence, and extract data in a list
    if len(liste_acc_val) == 3:  # check is lengt of recorded values on one line is 3 : x, y, and z.
        # If not (because not complete) this if avoid a bug and dont use it...

        # meaning part
        if axis == 0:
            list_to_meanX.append(int(liste_acc_val[1]))
        if axis == 1:
            list_to_meanY.append(int(liste_acc_val[0]))

    else:
        continue

    if axis == 0:
        if len(
                list_to_meanX) == num_val_mean:  # when a list reaches num-val_mean : meaning starts and produces x_m or y_m
            n_m = int(mean(list_to_meanX))  # n_m will be the meaned value
            list_to_meanX = []  # putting the xlist to 0
    if axis == 1:
        if len(
                list_to_meanY) == num_val_mean:  # when a list reaches num-val_mean : meaning starts and produces x_m or y_m
            n_m = int(mean(list_to_meanY))  # n_m will be the meaned value
            list_to_meanY = []  # putting the xlist to 0

    lmin = int(
        0)  # resquale the values of lmin (=0), lmax = nmax-nmin and lact is the instantaneous position of axis sensor
    lmax_temp = nmax - nmin
    lmax = lmax_temp
    lact = n_m - nmin
    pclact = lact / lmax  # a percentage _ = resquale from 0 to 1


    if xp < float(pclact * w_screen) and xp < w_screen-60: xp += nb_of_px  # go right and down util x=w_screen
    if xp > float(pclact * w_screen) and xp > 5: xp -= nb_of_px  # go_left and up until x=0

    screen.blit(backgr,(0,0))

    lanceur.move(2) # movement of top-launcher , in braquets : speed
    lanceur.afficher() # displaying of top-launcher

    for chaqueobjet in dico.values():  # look into the dictionnary the differents existing objects.
        chaqueobjet.move()  # change the postition
        chaqueobjet.afficher()  # print it
        chaqueobjet.collide() #check a collision

    if random() < 0.01:  # random generation of objects
        nomtemp = str("object" + str(objectnumber))  # each object will have a id
        dico[nomtemp] = ObjetsLances(lanceur.distancex, 50)  # add the object in the dictionnary
        objectnumber = objectnumber + 1  # increase of one the next id


    texttoprint1 = police.render(str(score_count), True, pygame.Color("#000000"))  # about the text that will be printed
    screen.blit(basketp, (xp,  h_screen * 0.9))
    screen.blit(texttoprint1, (w_screen * 0.9, 20))  # the prit of text (scoring)
#    pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(xp, h_screen * 0.9, 60, 60))  # the MPU6050' controlled item

    pygame.display.flip() # screen refresh

    screen.fill((255, 255, 255))  # fullfillment of the screen with a color
    clock.tick(90) #speed of looping

ser.close()  # close port