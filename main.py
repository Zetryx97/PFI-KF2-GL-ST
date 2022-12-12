from radionavigation import Radionavigation
from moteur import Moteur
from time import sleep
from navigation_inertielle import Navigation
import threading



moteur = Moteur()
navi_inertielle = Navigation()

th_navi_inertielle = threading.Thread(target=navi_inertielle.orientation_position)
th_navi_inertielle.start()
sleep(5)
navi_inertielle.etat = 1
angle = 180
while navi_inertielle.angle_robot() > angle + 2   or navi_inertielle.angle_robot() < angle - 2:
    print(navi_inertielle.angle_robot())
    moteur.tourner_droite(0.5)
moteur.arreter()
sleep(5)
navi_inertielle.doit_continuer = False