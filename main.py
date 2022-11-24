from moteur import Moteur
from lidar import Lidar
from time import sleep


moteur = Moteur()
lidar = Lidar()


lidar.détecter_objet()
sleep(0.5)
lidar.détecter_objet()
sleep(0.5)
lidar.détecter_objet()
sleep(0.5)

print("C'est fini")
  