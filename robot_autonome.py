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
        self.orientation = 360
        self.INTERVALLE_ACCEPTATION = 0.2
        self.INTERVALLE_ANGLE = 2
        self.ANGLE_ROTATION = 360
        th_navi_inertielle = threading.Thread(target=self.navi_inertielle.orientation_position)
        th_navi_inertielle.start()
        th_radio_navigation = threading.Thread(target=self.radio_navigation.demarrer_position)
        th_radio_navigation.start()
        #th_lidar = threading.Thread(target=self.lidar.détecter_objet)
        #th_lidar.start()


    def demarrer_robot_autonome(self,position_cible_x,position_cible_y):
        sleep(3)
        while self.robot_en_marche :
            sleep(0.5)
            # rouler nos condition pour le mouvement: si objet detecter on freine ; algorythme de deplacement
            if(abs(float(self.radio_navigation.pos_robot_x) - position_cible_x) < self.INTERVALLE_ACCEPTATION and abs(float(self.radio_navigation.pos_robot_y) - position_cible_y) < self.INTERVALLE_ACCEPTATION) :
                self.robot_en_marche = False
                self.navi_inertielle.etat = 0
                self.moteur.freiner()
            elif(self.lidar.objet_détecter):
                self.navi_inertielle.etat = 0
                self.moteur.freiner()
            elif (float(self.radio_navigation.pos_robot_x) < position_cible_x) and (abs(float(self.radio_navigation.pos_robot_x) - position_cible_x) > self.INTERVALLE_ACCEPTATION):
                # avancer vers 90 degres :: EST
                self.navi_inertielle.etat = 1
                self.Orienter_robot(270)
                self.moteur.avancer(0.3)
            elif (float(self.radio_navigation.pos_robot_x) > position_cible_x) and (abs(float(self.radio_navigation.pos_robot_x) - position_cible_x) > self.INTERVALLE_ACCEPTATION):
                # avancer vers 270 degres :: OUEST
                self.navi_inertielle.etat = 1
                self.Orienter_robot(90)
                self.moteur.avancer(0.3)
            elif (float(self.radio_navigation.pos_robot_y) < position_cible_y) and (abs(float(self.radio_navigation.pos_robot_y) - position_cible_y) > self.INTERVALLE_ACCEPTATION):
                # avancer vers 0 degres :: NORD
                self.navi_inertielle.etat = 1
                self.Orienter_robot(0)
                self.moteur.avancer(0.3)
            elif (float(self.radio_navigation.pos_robot_y) > position_cible_y) and (abs(float(self.radio_navigation.pos_robot_y) - position_cible_y) > self.INTERVALLE_ACCEPTATION):
                # avancer vers 180 degres :: SUD
                self.navi_inertielle.etat = 1
                self.Orienter_robot(180)
                self.moteur.avancer(0.3)
            #self.navi_inertielle.etat = 0
            #print("---- X and Y ----")
            #print(self.radio_navigation.pos_robot_x)
            #print(self.radio_navigation.pos_robot_y)
        #se repositioner vers 0 degres pour le prochain point
        #self.navi_inertielle.etat = 1
        #self.Orienter_robot(0)
        # Ferme le robot
        self.moteur.arreter()
        self.navi_inertielle.etat = 0
        self.robot_en_marche = True
    
    def Orienter_robot(self,orientation_cible):
        # Tourner droite 0 -> 360 // anti-horraire
        # Tourner a gauche 0 -> 90 // horaire
        orientation_cible_min = orientation_cible -  self.INTERVALLE_ANGLE
        orientation_cible_max = orientation_cible +  self.INTERVALLE_ANGLE
        angle = self.navi_inertielle.angle_robot()
        if(angle < orientation_cible_max and angle > orientation_cible_min):
            return None

        if orientation_cible == 0:
            while self.navi_inertielle.angle_robot() < self.ANGLE_ROTATION - self.INTERVALLE_ANGLE and self.navi_inertielle.angle_robot() > orientation_cible_max and self.orientation != 0:
                if(self.navi_inertielle.angle_robot() < orientation_cible_max * 45 ) :
                    self.moteur.tourner_droite(0.4)
                else:
                    self.moteur.tourner_gauche(0.4)
            self.moteur.freiner()
        elif(angle < orientation_cible):
            # tourner a gauche
            while self.navi_inertielle.angle_robot() < orientation_cible_min and (self.orientation != orientation_cible or abs(self.navi_inertielle.angle_robot() - orientation_cible) > 5):
                self.moteur.tourner_gauche(0.4)
                #print(self.navi_inertielle.angle_robot())
            self.moteur.freiner()
        else:
            #tourner a droite
            while self.navi_inertielle.angle_robot() > orientation_cible_max and (self.orientation != orientation_cible or abs(self.navi_inertielle.angle_robot() - orientation_cible) > 5):
                self.moteur.tourner_droite(0.4)
                #print(self.navi_inertielle.angle_robot())
            self.moteur.freiner()
        self.orientation = orientation_cible


    def fermer_robot(self):
        self.radio_navigation.doit_continuer = False
        self.lidar.doit_continuer = False
        self.navi_inertielle.doit_continuer = False



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
    robot_autonome.demarrer_robot_autonome(8.85,2)
    robot_autonome.demarrer_robot_autonome(7.5,1.8)
    robot_autonome.demarrer_robot_autonome(6.75,0.3)
    robot_autonome.demarrer_robot_autonome(8.85,0)
    #robot_autonome.Orienter_robot(90)
    robot_autonome.fermer_robot()


  