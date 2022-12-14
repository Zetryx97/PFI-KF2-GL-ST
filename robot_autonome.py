#Gabriel Lessard - Samy Tétrault
#PFI KF2

from moteur import Moteur
from lidar import Lidar
from navigation_inertielle import Navigation
from radionavigation import Radionavigation
from time import sleep
import threading


class Robot_Autonome :
    def __init__(self):
        self.moteur = Moteur()
        self.lidar = Lidar()
        self.navi_inertielle = Navigation()
        self.radio_navigation = Radionavigation()
        self.robot_en_marche = True
        self.orientation = 0
        self.INTERVALLE_ACCEPTATION = 0.2
        self.INTERVALLE_ANGLE = 2


    def demarrer_robot_autonome(self,position_cible_x,position_cible_y):
        #th_lidar = threading.Thread(target=self.lidar.détecter_objet)
        th_navi_inertielle = threading.Thread(target=self.navi_inertielle.orientation_position)
        th_radio_navigation = threading.Thread(target=self.radio_navigation.demarrer_position)
        #th_lidar.start()
        th_navi_inertielle.start()
        th_radio_navigation.start()
        sleep(3)
        while self.robot_en_marche :
            sleep(0.5)
            # rouler nos condition pour le mouvement: si objet detecter on freine ; algorythme de deplacement
            if(self.lidar.objet_détecter):
                self.navi_inertielle.etat = 0
                self.moteur.freiner()
            elif (float(self.radio_navigation.pos_robot_x) < position_cible_x) and (float(self.radio_navigation.pos_robot_x) - position_cible_x > self.INTERVALLE_ACCEPTATION):
                # avancer vers 90 degres :: EST
                self.navi_inertielle.etat = 1
                self.Orienter_robot(90)
                self.moteur.avancer(0.4)
            elif (float(self.radio_navigation.pos_robot_x) > position_cible_x) and (float(self.radio_navigation.pos_robot_x) - position_cible_x > self.INTERVALLE_ACCEPTATION):
                # avancer vers 270 degres :: OUEST
                self.navi_inertielle.etat = 1
                self.Orienter_robot(270)
                self.moteur.avancer(0.4)
            elif (float(self.radio_navigation.pos_robot_y) < position_cible_y) and (float(self.radio_navigation.pos_robot_y) - position_cible_y > self.INTERVALLE_ACCEPTATION):
                # avancer vers 0 degres :: NORD
                self.navi_inertielle.etat = 1
                self.Orienter_robot(0)
                self.moteur.avancer(0.4)
            elif (float(self.radio_navigation.pos_robot_y) > position_cible_y) and (float(self.radio_navigation.pos_robot_y) - position_cible_y > self.INTERVALLE_ACCEPTATION):
                # avancer vers 180 degres :: SUD
                self.navi_inertielle.etat = 1
                self.Orienter_robot(180)
                self.moteur.avancer(0.4)
            sleep(0.5)
            self.moteur.freiner()
            self.navi_inertielle.etat = 0
            print("---- X and Y ----")
            print(self.radio_navigation.pos_robot_x)
            print(self.radio_navigation.pos_robot_y)
        #se repositioner vers 0 degres pour le prochain point
        self.navi_inertielle.etat = 1
        self.Orienter_robot(0)
        # Ferme le robot
        self.moteur.arreter()
        self.navi_inertielle.etat = 0
        self.lidar.doit_continuer = False
        self.navi_inertielle.doit_continuer = False
        self.radio_navigation.doit_continuer = False
    
    def Orienter_robot(self,orientation_cible):
        orientation_cible_min = orientation_cible -  self.INTERVALLE_ANGLE
        orientation_cible_max = orientation_cible +  self.INTERVALLE_ANGLE
        if(orientation_cible_min < 0):
            orientation_cible_min = orientation_cible_min + 360
        if(orientation_cible_max > 360):
            orientation_cible_max = orientation_cible_max - 360

        if(self.navi_inertielle.angle_robot() < orientation_cible_max or self.navi_inertielle.angle_robot() > orientation_cible_min):
            return None
        elif(orientation_cible != 0):
            #tourner jusqua temps d'être égal a l'angle
            while self.navi_inertielle.angle_robot() > orientation_cible_max or self.navi_inertielle.angle_robot() < orientation_cible_min:
                self.moteur.tourner_droite(0.6)
            self.moteur.freiner()
        else :
            while self.navi_inertielle.angle_robot() > orientation_cible_max or self.navi_inertielle.angle_robot() < orientation_cible_min:
                self.moteur.tourner_droite(0.6)
            self.moteur.freiner()
        #reecrire pour corriger le petit erreur d'angle


# --- Étape à suivre pour le main ---
# Minimum 3 thread : th1 = lidar , th2 = navigation inertielle, th3 = radionavigation, th4 = traiter les info des autres threads
# Th1 : vas verifier que il n'y a pas un object devant le robot et indique dans un etat global qu'un object est detecter
# Th2 : vas pouvoir donner l'angle que le robot fait face pour garder en memoire la direction
# Th3 : vas etre intialiser avec la position de depart et vas constament mettre a jour sa position
# Th4 : "Le Main des thread" qui vas rouler avec certaine condition
#       Si Th1 detecte un objet, arreter et changer de direction
#       Vas determiner un chemin simple a suivre selon l'avant du robot (Th2) et vas se deplacer vers la cible du th3
#       Algorythme de deplacement : {x1 < x2 : Vers 0 degres} , {x1 > x2 : vers 180 degres} , {y1 < y2 : Vers 90 degres} ,  {y1 > y2 : Vers 270 degres}
#       Lorsque Position_Robot == Position_cible, arreter le programme!

if __name__ == "__main__":
    robot_autonome = Robot_Autonome()
    robot_autonome.demarrer_robot_autonome(8.85,0)
    #robot_autonome.demarrer_robot_autonome(8.85,2)
    #robot_autonome.demarrer_robot_autonome(7.5,1.8)
    #robot_autonome.demarrer_robot_autonome(6.75,0.3)
    #robot_autonome.demarrer_robot_autonome(5.75,1)


  