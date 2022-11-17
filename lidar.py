#Gabriel Lessard - Samy Tétrault
#PFI KF2

import PyLidar3
from moteur import Moteur



class Lidar:

    def __init__(self):
        self.moteur_robot = Moteur()
        self.port = "/dev/ttyUSB0"
        self.obj_lidar = PyLidar3.YdLidarX4(self.port)
        self_objet_détecter = False

    def détecter_objet(self):
        return None
        