from moteur import Moteur
from time import sleep


moteur = Moteur()



while True:
    moteur.avancer(0.3)
    sleep(2)
    moteur.reculer(0.3)
    sleep(2)
    moteur.tourner_droite(0.4)
    sleep(5)
    moteur.tourner_gauche(0.4)
    sleep(5)
    break
print("C'est fini")
  