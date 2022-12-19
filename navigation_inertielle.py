#Gabriel Lessard - Samy Tétrault
#PFI KF2
import time
from time import sleep
from icm20948 import ICM20948

class Navigation:
    def __init__(self):
        self.imu = ICM20948()
        self.INTERVALLE_MESURE = 0.05
        self.IMMOBILE = 0
        self.FENETRE = 10
        self.FORCE_G = 9.80665
        self.MOUVEMENT = 1 #IMMOBILE = 0 , EN MOUVEMENT = 1 ou 2 (avance ou tourne)
        self.DEGRES_CERCLE = 360
        self.doit_continuer = True
        self.gx_biais = 0
        self.ay_biais = 0
        self.tab_fenetre_gx = [0]
        self.tab_fenetre_ay = [0]
        self.last_gx = 0
        self.last_ay = 0
        self.rotation = 0
        self.last_delta_temps = None
        self.angle_x = 0

        self.etat = 0

    def orientation_position(self): #À remodifier
        #NB:
        #ax, ay,az = Une accélération en fraction de g selon un des axes
        #gx,gy,gz = Une vitesse de rotation en DPS selon un des axes 
        #DPS = Degré Par Seconde        
        self.last_delta_temps = time.perf_counter()
        while self.doit_continuer :
            sleep(self.INTERVALLE_MESURE)
            ax, ay, az, gx, gy, gz = self.imu.read_accelerometer_gyro_data()
            #start counter
            delta_temps = time.perf_counter()
            
            if  self.etat == self.IMMOBILE:
                self.gx_biais = gx
                self.ay_biais = ay
                self.ajout_val_tab_moyenne(self.tab_fenetre_gx,self.gx_biais)
                self.ajout_val_tab_moyenne(self.tab_fenetre_ay,self.ay_biais)                
            elif self.etat == self.MOUVEMENT:
                gx_corriger = gx - self.calculer_moyenne_fenetrer(self.tab_fenetre_gx)
                self.angle_x += (delta_temps - self.last_delta_temps) * (gx_corriger + self.last_gx - self.calculer_moyenne_fenetrer(self.tab_fenetre_gx)) / 2
            self.last_gx = gx
            self.last_ay = ay
            self.last_delta_temps = delta_temps

    def angle_robot(self):
        if(self.angle_x > self.DEGRES_CERCLE):
            self.angle_x -= self.DEGRES_CERCLE
        if(self.angle_x < 0):
            self.angle_x += self.DEGRES_CERCLE
        return self.angle_x

    def calculer_moyenne_fenetrer(self,tab_moyenne):
        moyenne = sum(tab_moyenne)/len(tab_moyenne)
        return (moyenne)
    
    def ajout_val_tab_moyenne(self,tab_fenetre,val):
        tab_fenetre.append(val)        
        if len(tab_fenetre)>self.FENETRE:
            del tab_fenetre[0]