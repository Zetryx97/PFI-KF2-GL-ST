#Gabriel Lessard - Samy Tétrault
#PFI KF2

from moteur import Moteur
from lidar import Lidar
from navigation_inertielle import Navigation
from radionavigation import Radionavigation
from time import sleep
import threading


class Robot_Autonome :
    def __init__(self,position_cible):
        self.moteur = Moteur()
        self.lidar = Lidar()
        self.navi_inertielle = Navigation()
        self.radio_navigation = Radionavigation()
        self.robot_en_marche = True
        self.position_cible = position_cible


    def demarrer_robot_autonome(self):
        th_lidar = threading.Thread(target=self.lidar.détecter_objet)
        th_navi_inertielle = threading.Thread(target=self.navi_inertielle.orientation_position)
        th_radio_navigation = threading.Thread(target=self.radio_navigation.demarrer_position)
        th_lidar.start()
        th_navi_inertielle.start()
        th_radio_navigation.start()
        while self.robot_en_marche :
            sleep(0.5)
        self.lidar.doit_continuer = False
        self.navi_inertielle.doit_continuer = False
        self.radio_navigation.doit_continuer = False

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




  