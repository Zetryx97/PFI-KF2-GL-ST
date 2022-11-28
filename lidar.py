#Gabriel Lessard - Samy Tétrault
#PFI KF2

import PyLidar3
from time import sleep



class Lidar:

    def __init__(self):
        self.obj_lidar = PyLidar3.YdLidarX4("/dev/ttyUSB0")
        self.objet_détecter = False
        self.dictio_données = None
        self.INTERVALLE_ANGLE_MIN = 160
        self.INTERVALLE_ANGLE_MAX = 220
        self.INTERVALLE_MAX_DÉTECT = 120
        self.doit_continuer = True

    def détecter_objet(self):
        while self.doit_continuer :
            sleep(1)
            if self.obj_lidar.Connect():
                gen = self.obj_lidar.StartScanning()
                while not self.objet_détecter:
                    data = next(gen)
                    sleep(1)
                    self.dictio_données: data[0:359]
                    angle_a_verifier = self.INTERVALLE_ANGLE_MIN
                    self.objet_détecter = False
                    while angle_a_verifier < self.INTERVALLE_ANGLE_MAX : 
                        if data[angle_a_verifier]/10 < self.INTERVALLE_MAX_DÉTECT:
                            print("Object detected  at angle :" + str(angle_a_verifier))
                            print(str(data[angle_a_verifier]))
                            self.objet_détecter = True
                        angle_a_verifier = angle_a_verifier + 1
                self.déconnecter_lidar()
            else:
                print("Erreur")
                self.obj_lidar.Reset()
    

    def déconnecter_lidar(self):
        self.obj_lidar.StopScanning()
        self.obj_lidar.Disconnect()

        