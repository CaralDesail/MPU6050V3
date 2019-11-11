import sys
import os
import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock

from kivy.uix.slider import Slider

"""Première partie : avec seulement une petite fenetre qui va attraper l'id utilisateur"""


class Lancement(App):
    def build(self):
        return LancementLayout()



class LancementLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(LancementLayout, self).__init__(**kwargs)

        self.title = 'Utilisateur'
        self.orientation = "vertical"
        self.padding=10
        self.spacing=10
        Window.size = (500, 150)
        self.add_widget(Label(text=" Quel est l'identifiant utilisateur ? ", size_hint_y=0.1))
        self.add_widget(Label(text=" (Format NPDDN) ", size_hint_y=0.1))

        self.username = TextInput(text='',
                                  font_size=28,
                                  size_hint_y=0.5,
                                  size_hint_x=1,
                                  multiline=False
                                  )
        self.username.bind(on_text_validate=self._suite)  # call _suite when enter is pressed after a text is printed
        self.add_widget(self.username)

        boutonsuite = Button(text='Valider', font_size=30, size_hint=(1, 0.3), pos_hint={400: 0.9})
        boutonsuite.bind(on_press=self._suite)
        self.add_widget(boutonsuite)

    def toDoWithText(self):
        global userId
        userId = self.username.text
        with open("ac_user", "w") as myactualuser:
            myactualuser.write(userId)


    def _suite(self, source):
        self.toDoWithText()
        App.get_running_app().stop()  # Stop Lancement_layout
        SuiteApp().run()  # starts the following screen


"""la suite"""


class SuiteApp(App):
    def build(self):

        return LayoutGeneral()

class LayoutGeneral(BoxLayout):

    def __init__(self, **kwargs):
        super(LayoutGeneral, self).__init__(**kwargs)

        self.nombredeniveaux=int(3)
        self.nombredegraines=int(20)

        superBox = BoxLayout(orientation='vertical',spacing= 10, padding=10)  # global box

        """bandeau du haut"""

        Window.size = (1280, 800)

        topbox1 = BoxLayout(orientation='horizontal', size_hint_y=0.1)  # top box will contain id and date

        textIdtoprint=str('Bonjour ')+str(userId)
        textID = Label(text=textIdtoprint,
                       font_size=15
                       )

        datetoprint = str(datetime.datetime.now().day) + str('-') + str(datetime.datetime.now().month) + str('-') + str(
            datetime.datetime.now().year)
        textdate = Label(text=datetoprint, size_hint_x=0.2)

        topbox1.add_widget(textID)
        topbox1.add_widget(textdate)

        """bandeau du bas"""

        horizontalBox = BoxLayout(orientation='horizontal',spacing= 10, padding=10)

        intravbox = BoxLayout(orientation='vertical',spacing= 10, padding=10)

        button1Calibration1D = Button(text="Calibration 1D", font_size=40, size_hint=(0.98, 0.4))
        button1Calibration1D.bind(on_release=self.button1)
        button2Calibration2D = Button(text="Calibration 2D", font_size=40, size_hint=(0.98, 0.4), background_color=[1,1,1,0.3])
        buttonboxPyou=BoxLayout(orientation='horizontal',spacing= 10, padding=10)
        button3Pyou = Button(text="Pyou", font_size=40, size_hint=(0.98, 1))
        button3Pyou.bind(on_release=self.button3)
        intrabuttonboxpyou=BoxLayout(orientation='vertical',spacing= 10, padding=10)
        button4CatchyP = Button(text="CatchY", font_size=40, size_hint=(0.98, 0.4))
        button4CatchyP.bind(on_release=self.button4)
        sllv=Slider(id="lv",min="1",max="3",value="3",value_track=True,step=1)
        sllv.bind(value=self.mavariableduslider1)
        self.lbsl=Label(text="3 niveaux",font_size=20)
        sl2scorep=Slider(id="scorep",min="5",max="50",value="20",value_track=True,step=5)
        sl2scorep.bind(value=self.mavariableduslider2)

        self.lbsl2 = Label(text="20 graines", font_size=20)

        textbas=Label(text="")

        intravbox.add_widget(button1Calibration1D)
        intravbox.add_widget(button2Calibration2D)
        intravbox.add_widget(buttonboxPyou)
        buttonboxPyou.add_widget(button3Pyou)
        buttonboxPyou.add_widget(intrabuttonboxpyou)
        intrabuttonboxpyou.add_widget(sllv)
        intrabuttonboxpyou.add_widget(self.lbsl)
        intrabuttonboxpyou.add_widget(sl2scorep)
        intrabuttonboxpyou.add_widget(self.lbsl2)
        intravbox.add_widget(button4CatchyP)
        intravbox.add_widget(textbas)

        #texte sur le côté droit
        with open("scores.txt", "r") as myscores:  # put it into a calibration_vars with date
            text_onside = myscores.read()
        textarchives = Label(text=text_onside, size_hint_x=0.4, valign='top', halign='auto')

        horizontalBox.add_widget(intravbox)
        horizontalBox.add_widget(textarchives)

        superBox.add_widget(topbox1)
        superBox.add_widget(horizontalBox)

        self.add_widget(superBox)

    def button1(self,*args):
        cmd = 'python Calibration1D.py'
        os.system(cmd)

    def button3(self,*args):
        cmd = 'python Pyou.py'
        os.system(cmd)

    def button4(self,*args):
        cmd = 'python CatchyP.py'
        os.system(cmd)

    def mavariableduslider1(self,*args):
        self.nombredeniveaux=str(int(args[1]))
        texteaafficherniveaux=self.nombredeniveaux + " niveau(x)"
        self.lbsl.text=texteaafficherniveaux
        with open("ParamsPyou", "w") as myfile:  # put it into a scores with date
            strsc = str(self.nombredeniveaux) + str(" ") + str(self.nombredegraines) + str(" ")
            myfile.write(strsc)

    def mavariableduslider2(self,*args):

        self.nombredegraines=str(int(args[1]))
        texteaaffichergraines=self.nombredegraines + " graines"
        self.lbsl2.text=texteaaffichergraines
        with open("ParamsPyou", "w") as myfile:  # put it into a scores with date
            strsc = str(self.nombredeniveaux) + str(" ") + str(self.nombredegraines) + str(" ")
            myfile.write(strsc)

Lancement().run()