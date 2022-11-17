#Gabriel Lessard - Samy Tétrault
#PFI KF2

import serial
import time


class Radionavigation:
    def __init__(self):
        self.ser = serial.Serial()
        self.ser.port = '/dev/ttyACM0'
        self.ser.baudrate = 115200
        self.ser.open()

    
    def obtenir_position_robot(self):
        #Démarrer la communication
        self.ser.write(b'\r\r') #séquence d'octets
        time.sleep(1)

        #Obtenir la position
        self.ser.write(b'lep\n')
        pos_robot = str(self.ser.readline())

        #Formater la position correctement
        pos_robot.split(',')
        pos_robot.replace(',', '-')

        return pos_robot


