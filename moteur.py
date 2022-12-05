#Gabriel Lessard - Samy Tétrault
#PFI KF2
from gpiozero import DigitalOutputDevice
from gpiozero import PWMOutputDevice
from time import sleep

class Moteur :
    def __init__(self):
        self.moteur_avg = DigitalOutputDevice(6) #roue avant gauche
        self.moteur_arg = DigitalOutputDevice(5) #roue arrière gauche

        self.moteur_avd = DigitalOutputDevice(15) #roue avant droite
        self.moteur_ard = DigitalOutputDevice(14) #roue arrière droite

        self.control_moteur_g = PWMOutputDevice(13) #permet d'allumer ou d'éteindre les 2 moteurs de gauche
        self.control_moteur_d = PWMOutputDevice(18) #permet d'allumer ou d'éteindre les 2 moteur de droite
    
    def avancer(self,speed):
        self.moteur_avg.on()#roue off = recule, on = avancer
        self.moteur_arg.off()#roue on = recule, off = avancer
        self.control_moteur_g.on()
        self.moteur_avd.on()
        self.moteur_ard.off()
        self.control_moteur_d.on()

        self.control_moteur_g.value = speed
        self.control_moteur_d.value = speed

    def reculer(self,speed):
        self.moteur_avg.off()
        self.moteur_arg.on()
        self.control_moteur_g.on()
        self.moteur_avd.off()
        self.moteur_ard.on()
        self.control_moteur_d.on()

        self.control_moteur_g.value = speed
        self.control_moteur_d.value = speed

    def tourner_droite(self,speed):
        self.moteur_avg.off()
        self.moteur_arg.on()
        self.control_moteur_g.on()
        self.moteur_avd.on()
        self.moteur_ard.off()
        self.control_moteur_d.on()

        self.control_moteur_g.value = speed
        self.control_moteur_d.value = speed

    def tourner_gauche(self,speed):
        self.moteur_avg.on()
        self.moteur_arg.off()
        self.control_moteur_g.on()
        self.moteur_avd.off()
        self.moteur_ard.on()
        self.control_moteur_d.on()

        self.control_moteur_g.value = speed
        self.control_moteur_d.value = speed

    def freiner(self):
        self.moteur_avg.on()
        self.moteur_arg.on()
        self.control_moteur_g.on()
        self.moteur_avd.on()
        self.moteur_ard.on()
        self.control_moteur_d.on()

    def arreter(self):
        self.moteur_avg.off()
        self.moteur_arg.off()
        self.control_moteur_g.off()
        self.moteur_avd.off()
        self.moteur_ard.off()
        self.control_moteur_d.off()