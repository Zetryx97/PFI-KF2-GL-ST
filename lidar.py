#Gabriel Lessard - Samy Tétrault
#PFI KF2

import PyLidar3
from time import sleep



class Lidar:

    def __init__(self):
        self.obj_lidar = PyLidar3.YdLidarX4("/dev/ttyUSB0")
        self.objet_détecter = False
        self.INTERVALLE_ANGLE_MIN = 175
        self.INTERVALLE_ANGLE_MAX = 185
        self.INTERVALLE_MAX_DÉTECT = 90
        self.doit_continuer = True

    def détecter_objet(self):
        while self.doit_continuer:
            sleep(1)
            if self.obj_lidar.Connect():
                gen = self.obj_lidar.StartScanning()
                data = next(gen)
                sleep(1)
                angle_a_verifier = self.INTERVALLE_ANGLE_MIN
                object_detecter_scan = False
                while angle_a_verifier < self.INTERVALLE_ANGLE_MAX : 
                    if data[angle_a_verifier]/10 < self.INTERVALLE_MAX_DÉTECT and data[angle_a_verifier]/10 != 0:
                        print("Object detected  at angle :" + str(angle_a_verifier))
                        print(str(data[angle_a_verifier]))
                        object_detecter_scan = True
                    angle_a_verifier = angle_a_verifier + 1
                self.obj_lidar.Disconnect()
                self.objet_détecter = object_detecter_scan
            else:
                print("Erreur")
                self.obj_lidar.Reset()
    

    def déconnecter_lidar(self):
        self.obj_lidar.StopScanning()
        self.obj_lidar.Disconnect()



if __name__ == "__main__":
    from moteur import Moteur
    import threading
    lidar = Lidar()
    moteur = Moteur()
    th_lidar = threading.Thread(target=lidar.détecter_objet)
    th_lidar.start()
    sleep(30)
    lidar.doit_continuer = False


        