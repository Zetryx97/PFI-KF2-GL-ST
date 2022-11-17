#Gabriel Lessard - Samy Tétrault
#PFI KF2

import time
from time import sleep
import threading
from moteur import Moteur
from icm20948 import ICM20948

class Navigation:
    def __init__(self):
        self.imu = ICM20948()
        self.INTERVALLE_MESURE = 0.05
        self.IMMOBILE = 0
        self.TRANSLATION = 1
        self.ROTATION = 2
        self.gx_biais = 0
        self.ay_biais = 0
        self.tab_fenetre_gx = [0]
        self.tab_fenetre_ay = [0]
        self.last_gx = 0
        self.last_ay = 0
        self.last_vy = 0
        self.FENETRE = 10
        self.FORCE_G = 9.80665
        self.position = 0
        self.rotation = 0
        self.last_delta_temps = None
        self.vy = 0
        self.y = 0
        self.angle_x = 0
        self.DEGRES_CERCLE = 360

    def orientation_position(self): #À remodifier
        #NB:
        #ax, ay,az = Une accélération en fraction de g selon un des axes
        #gx,gy,gz = Une vitesse de rotation en DPS selon un des axes 
        #DPS = Degré Par Seconde        
        self.last_delta_temps = time.perf_counter()
        while self.deplacement_robot.doit_lire_touche :
            sleep(self.INTERVALLE_MESURE)
            ax, ay, az, gx, gy, gz = self.imu.read_accelerometer_gyro_data()
            #start counter
            delta_temps = time.perf_counter()
            etat = self.deplacement_robot.etat_robot
            if  etat == self.IMMOBILE:
                self.gx_biais = gx
                self.ay_biais = ay
                self.ajout_val_tab_moyenne(self.tab_fenetre_gx,self.gx_biais)
                self.ajout_val_tab_moyenne(self.tab_fenetre_ay,self.ay_biais)
                self.last_vy = 0
                self.vy = 0
                                
            elif etat == self.ROTATION:
                gx_corriger = gx - self.calculer_moyenne_fenetrer(self.tab_fenetre_gx)
                self.angle_x += (delta_temps - self.last_delta_temps) * (gx_corriger + self.last_gx - self.calculer_moyenne_fenetrer(self.tab_fenetre_gx)) / 2
            self.last_gx = gx
            self.last_ay = ay
            self.last_delta_temps = delta_temps

    def get_orientation(self):
        return None

    def demarer_robot_navigation(self):
        th_orientation = threading.Thread(target=self.orientation_position)
        th_deplacement = threading.Thread(target=self.deplacement_robot.deplacer_robot)
        th_deplacement.start()
        sleep(1)
        th_orientation.start()
        while self.deplacement_robot.doit_lire_touche :
            print('Position :' + str(self.y))
            if(self.angle_x > self.DEGRES_CERCLE)
                self.angle_x -= self.d
            print('Rotation :' + str(self.angle_x))
            sleep(0.1)

    def calculer_moyenne_fenetrer(self,tab_moyenne):
        moyenne = sum(tab_moyenne)/len(tab_moyenne)
        return (moyenne)
    
    def ajout_val_tab_moyenne(self,tab_fenetre,val):
        tab_fenetre.append(val)        
        if len(tab_fenetre)>self.FENETRE:
            del tab_fenetre[0]