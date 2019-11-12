import re
from statistics import mean
import math
import pygame
from serialpart import *
import serialpart

pygame.init()
h_screen = 1024
w_screen = 1024

screen = pygame.display.set_mode((w_screen, h_screen))

backscreen = pygame.image.load("ressources/test/space1.png").convert()
backscreen = pygame.transform.scale(backscreen, (w_screen, h_screen))
fenetre = pygame.display.set_mode((w_screen, h_screen))

done = False
screen = pygame.display.set_mode((h_screen, w_screen))
rectScreen = screen.get_rect()

num_val_mean = 5
clock = pygame.time.Clock()
police = pygame.font.Font(None, 72)

x = h_screen // 2
y = w_screen // 2

print(ser.readline())
print(ser.readline())
print(ser.readline())

# initial positions of current x y and z
x_m = int(0)
y_m = int(0)

list_to_meanX = []  # create a list in wich we'll put "num_val_mean" values before meaning it.
list_to_meanY = []  # the same with y

with open("Calibration2D.txt", "r") as mycalfile:  # put it into a calibration_vars
    text_of_limits = mycalfile.read()
    list_of_limits = text_of_limits.split()
    print(list_of_limits)


class Player(pygame.sprite.Sprite):
    # This class represents the player. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height, list_of_limits):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the item, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.origin = pygame.Surface([width, height])
        self.origin = pygame.image.load("ressources/test/spaceship.png").convert_alpha() #the name of the sprite
        self.original = pygame.transform.scale(self.origin, (40, 80))

        # import list of limits
        self.list_of_limits = list_of_limits
        # resquale the limits
        self.newXmax = int(list_of_limits[3]) - int(list_of_limits[2])
        self.newYmax = int(list_of_limits[5]) - int(list_of_limits[4])

        # Draw the image (a rectangle here)
        # pygame.draw.rect(self.original, color, [0, 0, width, height])

        self.image = pygame.transform.scale(self.original, (20, 40))

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def update(self, x_m, y_m):
        self.vitesse = 4  # speed factor
        self.newX = x_m - int(self.list_of_limits[2])  # rescale the x value from 0 to 36000
        self.rapnewX = (self.newX / self.newXmax) * 2 - 1  # scale in relation with max value -> the fraction'll been between -1 and 1

        self.newY = y_m - int(self.list_of_limits[4])  # rescale the y value from 0 to 36000
        self.rapnewY = (self.newY / self.newYmax) * 2 - 1  # scale in relation with max value -> the fraction'll been between -1 and 1
        # print("Rapport X: ", self.rapnewX," Rapport Y: ", self.rapnewY)

        self.puissance = (abs(self.rapnewX) + abs(
            self.rapnewY)) / 2  # power of vector (depending on the sum of inclination of x and y). From 0 to 1.
        # print(" Longueur : ", self.puissance)

        anglerad =math.atan2(self.rapnewX, self.rapnewY)
        angledeg = ((180) / math.pi) * anglerad #calcul of angle for sprite rotation
        print("en degrès : ",angledeg," et en radians : ", anglerad)

        self.image = pygame.transform.rotate(self.original, angledeg) #dehach to rotate the sprite


        if self.puissance > 0.3:
            self.rect.x = self.rect.x + ((self.rapnewX / 2) * self.vitesse * self.puissance)
            self.rect.y = self.rect.y + ((self.rapnewY / 2) * self.vitesse * self.puissance)





all_sprites = pygame.sprite.Group()  # group creation
player = Player((255, 0, 0), 100, 100, list_of_limits)  # from module base_player
player.rect.x = 200  # where starts the rect
player.rect.y = 300  # where starts the rect
all_sprites.add(player)  # add sprite player to group all_sprites

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

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

        list_to_meanX = []  # putting the xlist to 0
        list_to_meanY = []  # putting the ylist to 0



    screen.fill((0, 0, 0))  # fullfillment of the screen with a color
    fenetre.blit(backscreen, (0, 0))
    player.update(x_m, y_m)
    all_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(60)

ser.close()  # close port
