#base of game with base_player import for player sprite


import re
from statistics import mean
import pygame
from serialpart import *
import base_player

pygame.init()
h_screen=1280
w_screen=840

done = False
screen = pygame.display.set_mode((h_screen, w_screen))
rectScreen = screen.get_rect()

num_val_mean = 5
clock = pygame.time.Clock()
police = pygame.font.Font(None, 72)

x = h_screen//2
y = w_screen//2

print(ser.readline())
print(ser.readline())
print(ser.readline())

# initial positions of current x y and z
x_m=int(0)
y_m=int(0)


list_to_meanX=[] #create a list in wich we'll put "num_val_mean" values before meaning it.
list_to_meanY=[] #the same with y

with open("../Calibration2D.txt", "r") as mycalfile:  # put it into a calibration_vars
    text_of_limits = mycalfile.read()
    list_of_limits = text_of_limits.split()
    print(list_of_limits)




all_sprites = pygame.sprite.Group() # group creation
player = base_player.Player((255, 0, 0),50,50,list_of_limits) # from module base_player
player.rect.x = 200 #where starts the rect
player.rect.y = 300 #where starts the rect
all_sprites.add(player) #add sprite player to group all_sprites


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    # reading part
    info_serial_tr=ser.readline() # basis reading from serial port
    liste_acc_val= re.findall("(.[0-9]+)",str(info_serial_tr)) # we simplify the sentence, and extract data in a list

    if len(liste_acc_val)==3 :
        # meaning part
        list_to_meanX.append(int(liste_acc_val[1]))
        list_to_meanY.append(int(liste_acc_val[0]))
    else :
        continue


    if len(list_to_meanX)==num_val_mean: #when a list reaches num-val_mean : meaning starts and produces x_m and y_m
        x_m=int(mean(list_to_meanX)) # x_m will be the meaned value
        y_m=int(mean(list_to_meanY)) # y_m will be the meaned value

        list_to_meanX = [] #putting the xlist to 0
        list_to_meanY = [] #putting the ylist to 0



    screen.fill((0, 0, 0)) # fullfillment of the screen with a color


    player.update(x_m,y_m)
    all_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(60)

ser.close()             # close port