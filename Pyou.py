
from serialpart import * #will import serialpart.py (with port name and baudrate)
import serialpart
import re
from statistics import mean
import pygame
import datetime

def aff_bird(seed_taken):
    if seed_taken:
        if x>w_screen*0.8:
            return pyaf_picore
        else:
            return pyaf_up
    else:
        return pyaf_down

pygame.init()
h_screen=800
w_screen=1280
screen = pygame.display.set_mode((w_screen, h_screen))
done = False
rectScreen = screen.get_rect()


num_val_mean = 3 # value of softener function
nb_of_px =20 # speed of the object (in px/while )
diff_factor=1.0 #a factor that will change the values of nmin/nmax
seed_taken=bool(False)
score1=False
score2=False
scorecount=int(0)
clock = pygame.time.Clock()
backscreen = pygame.image.load("ressources/compoglobale.jpg").convert()
backscreen = pygame.transform.scale(backscreen, (w_screen, h_screen))
pyaf_down = pygame.image.load("ressources/pyaf_down.png").convert_alpha()
pyaf_up = pygame.image.load("ressources/pyaf_up.png").convert_alpha()
pyaf_picore = pygame.image.load("ressources/pyaf_picore.png").convert_alpha()
fenetre = pygame.display.set_mode((w_screen, h_screen))
police = pygame.font.Font(None, 72) #size of the font


x = h_screen//4
y = w_screen//4

# initial positions of current x y
n_m=int(0)


list_to_meanX=[] #create a list in wich we'll put "num_val_mean" values before meaning it.
list_to_meanY=[] #the same with y

print(ser.readline())
print(ser.readline())

with open("ac_user", "r") as myuser:  # put it into a calibration_vars
    ac_us = myuser.read()

with open("Calibration1D.txt", "r") as mycalfile:  # put it into a calibration_vars
    text_of_cal = mycalfile.read()
    list_of_cal1D = text_of_cal.split()
    print(list_of_cal1D)

axis=int(list_of_cal1D[0]) #axis will be 0 if x, 1 if y
basis_value=int(list_of_cal1D[1]) #the value on axis of neutral articulation position
nmin=int(list_of_cal1D[2])*diff_factor #minimum recorded value time difficultyfactor
nmax=int(list_of_cal1D[3])*diff_factor #maximum recorded value time difficultyfactor


with open("ParamsPyou", "r") as myuser:  # get the params informations to count the number of moves to succed the game.
    listtoreadParams = myuser.read()
    list_of_params = listtoreadParams.split()
    moves_to_reach=int(list_of_params[0])*int(list_of_params[1]) # moves_to_reach is this number ...


#ressources for the counter
backtab = pygame.image.load("ressources/dynamic_count_bar/table.png").convert_alpha() #import the wood style backtab
tbacktabw=int(w_screen*0.3)
tbacktabh=int(h_screen*0.2)
backtab = pygame.transform.scale(backtab, (tbacktabw,tbacktabh ))

countgback = pygame.image.load("ressources/dynamic_count_bar/moves.png").convert_alpha() #import the back of counter
tcountgbackw=int(w_screen*0.07)
tcountgbackh=int(h_screen*0.1)
countgback = pygame.transform.scale(countgback, (tcountgbackw,tcountgbackh ))

bgbar = pygame.image.load("ressources/dynamic_count_bar/bgbar.png").convert_alpha() #import the back of counter
tbgbarw=int(w_screen*0.25)
tbgbarh=int(h_screen*0.05)
bgbar = pygame.transform.scale(bgbar, (tbgbarw,tbgbarh ))




def print_dyn_count_bar(): #counter printing function
    gbar = pygame.image.load("ressources/dynamic_count_bar/gbar.png").convert_alpha()  # import the picture
    tgbarw = int(w_screen * 0.25 * (int(scorecount) / moves_to_reach)) #change the size according to the score / moves_t_r
    tgbarh = int(h_screen * 0.035)
    gbar = pygame.transform.scale(gbar, (tgbarw, tgbarh))

    fenetre.blit(backtab, (w_screen*0.70, 0))#where woodbacktab is printed
    fenetre.blit(countgback, (w_screen*0.75, h_screen*0.10))#where woodbacktab is printed
    fenetre.blit(bgbar, (w_screen*0.725, h_screen*0.02))#where woodbacktab is printed
    fenetre.blit(gbar, (w_screen*0.73, h_screen*0.03))#where woodbacktab is printed


def saving_process(ac_us,scorecount): #will use ac_us as name of user and scorecount to save it in file when called.
    with open("scores.txt", "r+") as myscorefile:  # put it into a scores with date
        text_rep = myscorefile.read()
        strsc = str("\n") + str(ac_us) + str(" ") + str("Pyou") + str(" ") + str(datetime.datetime.now().day) + str(
            '-') + str(datetime.datetime.now().month) \
                + str('-') + str(datetime.datetime.now().year) + str(" ") + str(datetime.datetime.now().hour) \
                + str(':') + str(datetime.datetime.now().minute) \
                + str(" ") + str(scorecount)
        myscorefile.write(strsc)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            saving_process(ac_us,scorecount) #call the saving function
            done = True
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]:
        saving_process(ac_us, scorecount) #call the saving function
        done=True

    # reading part
    liste_acc_val=serialpart.simpleard_to_xyz_list()

    if len(liste_acc_val)==3 : #check is lengt of recorded values on one line is 3 : x, y, and z.
        # If not (because not complete) this if avoid a bug and dont use it...

        # meaning part
        if axis == 0 :
            list_to_meanX.append(int(liste_acc_val[1]))
        if axis == 1 :
            list_to_meanY.append(int(liste_acc_val[0]))


    else :
        continue

    if axis == 0 :
        if len(list_to_meanX)==num_val_mean: #when a list reaches num-val_mean : meaning starts and produces x_m or y_m
            n_m=int(mean(list_to_meanX)) # n_m will be the meaned value
            list_to_meanX = []  # putting the xlist to 0
    if axis == 1 :
        if len(list_to_meanY)==num_val_mean: #when a list reaches num-val_mean : meaning starts and produces x_m or y_m
            n_m=int(mean(list_to_meanY)) # n_m will be the meaned value
            list_to_meanY = []  # putting the xlist to 0


    lmin=int(0) #resquale the values of lmin (=0), lmax = nmax-nmin and lact is the instantaneous position of axis sensor
    lmax_temp=nmax-nmin
    lmax=lmax_temp
    lact=n_m-nmin
    pclact=lact/lmax # a percentage _ = resquale from 0 to 1

#    print("X est à {} alors que pclact*w_screen est à {}".format(x,pclact*w_screen))

    if x < float(pclact*w_screen) and x<w_screen*0.83 : x+=nb_of_px #go right and down util x=w_screen*.9
    if x > float(pclact*w_screen) and x>w_screen*0.05 : x-=nb_of_px #go_left and up until x=w scree*0.01

    if x>w_screen*0.80 :
        seed_taken=True
        score1=True
    if x<w_screen*0.1 :
        seed_taken=False
        score2=True

    if score1 and score2 and seed_taken==False: #algo about scoring, it uses the fact that bird reached 2 sides and no seed
        scorecount+=1
        score1=False
        score2=False
        print(scorecount)
    texttoprint1= police.render(str(scorecount), True, pygame.Color("#000000")) #about the text that will be printed


    fenetre.blit(backscreen, (0, 0))
    print_dyn_count_bar()
    screen.blit(texttoprint1, (w_screen*0.77, h_screen*0.14)) #the prit of text (scoring)
    fenetre.blit(aff_bird(seed_taken), (x, x/1.6)) #use the function aff_bird to chose the picture, and position of bird

    pygame.display.flip()

    clock.tick(90)

ser.close()             # close port