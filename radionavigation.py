#Gabriel Lessard - Samy Tétrault
#PFI KF2

import serial
from time import sleep


class Radionavigation:
    def __init__(self):
        self.ser = serial.Serial()
        self.ser.port = '/dev/ttyACM0'
        self.ser.baudrate = 115200
        self.ser.open()
        self.position_robot = None #Référence sur la position du robot en Tout temps
        self.doit_continuer = True

    
    def obtenir_position_robot(self):
        #Démarrer la communication
        self.ser.write(b'\r\r') #séquence d'octets
        sleep(1)

        #Obtenir la position
        self.ser.write(b'lep\n')
        pos_robot = str(self.ser.readline())

        #Formater la position correctement
        pos_robot.split(',')
        pos_robot.replace(',', '-')

        self.position_robot = pos_robot #retourne un tuple de 4 ou 5 éléments: (possiblement pos),Val X, Val Y, Val Z, val pourcentage de la précision des données reçues

    def demarrer_position(self):
        while self.doit_continuer: 
            self.obtenir_position_robot()
            sleep(1)
        


