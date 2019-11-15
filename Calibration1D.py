"""
This is a part of the MPU 6050 Project
1D Calibration program that will takes the axis , zero position, and min/max of selected axis
in 4 steps. It will put the information in a current used file (Calibration1D.txt), and an archive one (CalArch.txt).
Alain Carrot
"""
import serialpart
from statistics import mean
import pygame
import sys
import datetime

def com_n_quit():
    for event in pygame.event.get():  # common command that asks for quitting system when user clics on QUIT icon.
        if event.type == pygame.QUIT:
            sys.exit()

with open("ac_user", "r") as myuser:  # put it into a calibration_vars
    ac_us = myuser.read()


pygame.init()
pygame.display.set_caption("Calibration1D")
screen = pygame.display.set_mode((1280, 800))


clock = pygame.time.Clock()
done1frame = False #condition of while 1
police = pygame.font.Font(None, 72) #size of the font
texte1frame1 = police.render("Merci de positionner le capteur.", True, pygame.Color("#000000"))
texte2frame1 = police.render("Appuyez sur Espace quand vous êtes prêt.", True, pygame.Color("#000000"))


while not done1frame : # First Frame
    clock.tick(90) #speed limit
    com_n_quit() #quit function
    pressed = pygame.key.get_pressed() #When user press a touch ... :
    if pressed[pygame.K_SPACE]: # SPACE will pass this "while" to second one.
        print("Space")
        done1frame=True


    screen.fill((255, 255, 255)) # fullfillment of the screen with a color
    screen.blit(texte1frame1, (50,200))
    screen.blit(texte2frame1, (50,300))
    pygame.display.flip()



from serialpart import * #will import serialpart.py (with port name and baudrate)

num_val_mean = 2 # value of the meaning of x, or y. Less will be more quick, more will me more smooth.

done2frame = False #condition of while 2
done3frame = False #condition of while 3
done4frame = False #condition of while 4

#list of differents values that this program will claim.
axe=int() #the ax value : x=0, y=1
valz=int() # the value of valz (z for zero)
nmin=int() # the value of minimum of x or y
nmax=int() # the value of maximum of x or y

color1 = (0, 128, 255) #blue
color2 = (0, 200, 255) #clear blue
color3 = (0, 80, 255) #dark blue


texte1frame2 = police.render("Quel axe souhaitez-vous utiliser ? ", True, pygame.Color("#000000"))
texte2frame2 = police.render("Appuyez sur X ou Y selon l'axe choisi", True, pygame.Color("#000000"))
texte3frame2 = police.render("X", True, pygame.Color("#000000"))
texte4frame2 = police.render("Y", True, pygame.Color("#000000"))
texte1frame3 = police.render("Veuillez laisser l'articulation en position neutre, ", True, pygame.Color("#000000"))
texte2frame3 = police.render("puis appuyez sur Espace", True, pygame.Color("#000000"))
texte1frame4 = police.render("Bougez l'articulation au maximum", True, pygame.Color("#000000"))
texte2frame4 = police.render("puis appuyez sur Entrer", True, pygame.Color("#000000"))


# initial positions of current x y
x_m=int()
y_m=int()
list_to_meanX=[] #create a list in wich we'll put "num_val_mean" values before meaning it.
list_to_meanY=[] #the same with y


# 3 first reading lines
print(ser.readline())
print(ser.readline())
print(ser.readline())




while not done2frame :
    clock.tick(300)
    com_n_quit() #quit function
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_x]:
        axe=0
        print("x selectionné", "axe vaut ",axe)
        done2frame = True
    if pressed[pygame.K_y]:
        axe=1
        print("y selectionné", "axe vaut ",axe)
        done2frame = True

    # reading part
    liste_acc_val=serialpart.simpleard_to_xyz_list()

    if len(liste_acc_val) == 3:
        # meaning part
        list_to_meanX.append(int(liste_acc_val[1]))
        list_to_meanY.append(int(liste_acc_val[0]))
    else:
        continue

    if len(list_to_meanX) == num_val_mean:  # when a list reaches num-val_mean : meaning starts and produces x_m and y_m
        x_m = int(mean(list_to_meanX))  # x_m will be the meaned value
        y_m = int(mean(list_to_meanY))  # y_m will be the meaned value
        print("x = ", x_m, "y = ", y_m)

        list_to_meanX = []  # putting the xlist to 0
        list_to_meanY = []  # putting the ylist to 0


    screen.fill((255, 255, 255))  # fullfillment of the screen with a color

    x_l = float(x_m) / 100
    y_l = float(y_m) / 100

    # print of different histograms with x/xmax and xmin and y / ymax and min
    pygame.draw.rect(screen, color1, pygame.Rect(300, 400, x_l, 50))
    pygame.draw.rect(screen, color1, pygame.Rect(900, 400, 50, y_l))

    screen.blit(texte1frame2, (50,50))
    screen.blit(texte2frame2, (50,150))
    screen.blit(texte3frame2, (300,700))
    screen.blit(texte4frame2, (900,700))

    pygame.display.flip()

    clock.tick(300)

while not done3frame: # third frame that will allow to set a valz (zero value ) of selected axis.
    clock.tick(300)
    com_n_quit() #quit function
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_SPACE]:
        if axe==0: valz=x_m
        if axe==1:valz=y_m

        print("valeur moyenne selectionnée, valz vaut : ", valz)
        nmin =valz
        nmax= valz
        done3frame = True

    # reading part
    liste_acc_val=serialpart.simpleard_to_xyz_list()

    if len(liste_acc_val) == 3:
        # meaning part
        list_to_meanX.append(int(liste_acc_val[1]))
        list_to_meanY.append(int(liste_acc_val[0]))
    else:
        continue

    if len(list_to_meanX) == num_val_mean:  # when a list reaches num-val_mean : meaning starts and produces x_m and y_m
        x_m = int(mean(list_to_meanX))  # x_m will be the meaned value
        y_m = int(mean(list_to_meanY))  # y_m will be the meaned value
        print("x = ", x_m, "y = ", y_m)

        list_to_meanX = []  # putting the xlist to 0
        list_to_meanY = []  # putting the ylist to 0


    screen.fill((255, 255, 255))  # fullfillment of the screen with a color

    x_l = float(x_m) / 100 # the good size for a visualisation of x
    y_l = float(y_m) / 100 # and y

    # if selected axis is 0, that is to say x, will print the corresponding histogram and letter, idem for y
    if axe==0:
        pygame.draw.rect(screen, color1, pygame.Rect(300, 400, x_l, 50))
        screen.blit(texte3frame2, (300, 700))
    if axe==1:
        pygame.draw.rect(screen, color1, pygame.Rect(900, 400, 50, y_l))
        screen.blit(texte4frame2, (900, 700))

    #in any case, prining of informations (what to do)
    screen.blit(texte1frame3, (50, 50))
    screen.blit(texte2frame3, (50, 150))

    pygame.display.flip()

    clock.tick(300)

while not done4frame:
    clock.tick(300)
    com_n_quit() #quit function
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_RETURN]:

        print(" Les valeurs selectionnées sont : ", nmin, nmax)
        done4frame = True

    # reading part
    liste_acc_val=serialpart.simpleard_to_xyz_list()

    if len(liste_acc_val) == 3:
        # meaning part
        list_to_meanX.append(int(liste_acc_val[1]))
        list_to_meanY.append(int(liste_acc_val[0]))
    else:
        continue

    if len(list_to_meanX) == num_val_mean:  # when a list reaches num-val_mean : meaning starts and produces x_m and y_m
        x_m = int(mean(list_to_meanX))  # x_m will be the meaned value
        y_m = int(mean(list_to_meanY))  # y_m will be the meaned value
        print("x = ", x_m, "y = ", y_m)

        list_to_meanX = []  # putting the xlist to 0
        list_to_meanY = []  # putting the ylist to 0


    screen.fill((255, 255, 255))  # fullfillment of the screen with a color


    # if selected axis is 0, that is to say x, will print the corresponding histogram and letter, idem for y
    if axe==0:
        x_l = float(x_m) / 100  # the good size for a visualisation of x
        pygame.draw.rect(screen, color1, pygame.Rect(300, 400, x_l, 50))#print actual x value
        pygame.draw.rect(screen, color2, pygame.Rect(300, 500, nmax/100, 50))#print nmax histogram
        pygame.draw.rect(screen, color3, pygame.Rect(300, 500, nmin/100, 50))# print nmin histogram
        screen.blit(texte3frame2, (300, 700)) #print "X"
        if x_m<nmin:
            nmin=x_m
            print("nmin descend à", nmin)
        if x_m>nmax:
            nmax=x_m
            print("nmax monte à", nmax)
    if axe==1:
        y_l = float(y_m) / 100  # the good size for visualisation of y
        pygame.draw.rect(screen, color1, pygame.Rect(900, 400, 50, y_l)) #print actual y value
        pygame.draw.rect(screen, color2, pygame.Rect(800, 400, 50, nmax/100)) #print nmax histogram
        pygame.draw.rect(screen, color3, pygame.Rect(800, 400, 50, nmin/100)) # print nmin histogram
        screen.blit(texte4frame2, (900, 700))  #Print "y"
        if y_m<nmin: # the selection of min value
            nmin=y_m
            print("nmin descend à", nmin)
        if y_m>nmax: # the selection of max value
            nmax=y_m
            print("nmax monte à", nmax)

    #in any case, prining of informations (what to do)
    screen.blit(texte1frame4, (50, 50))
    screen.blit(texte2frame4, (50, 150))

    pygame.display.flip()

    clock.tick(300)

calibration_vars=str(axe)+str(" ")+str(valz)+str(" ")+str(nmin)+str(" ")+str(nmax)+str(" ")+str(ac_us) #create the line with the 4 values

with open("Calibration1D.txt", "w") as mycalfile:  # put it into a calibration_vars
    mycalfile.write(calibration_vars)


with open("cal_arch.txt", "r+") as mycalarchfile:  # put it into a calibration_vars with date
    text_rep = mycalarchfile.read()
    cal_arch =  str("\n")+ str(datetime.datetime.now()) + str(" ") + str(calibration_vars) + str("\n")
    mycalarchfile.write(cal_arch)



ser.close()             # close port

sys.exit()