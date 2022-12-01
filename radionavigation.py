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
        self.ser.write(b'\r\r') #commande shell
        sleep(1)
        self.ser.write(b'lep\n')#commande shell
        self.pos_robot_x = None
        self.pos_robot_y = None
        self.pos_robot_z = None
        self.pourcentage_precis = None
        self.doit_continuer = True


    def show_position_robot(self):
        data = str(self.ser.readline())

        #Convert data
        self.updatePosRobot(data)

        print("POS: ")
        print(self.pos_robot_x)
        print(self.pos_robot_y)
        print(self.pos_robot_z)
        print(self.pourcentage_precis)
        

        

    def updatePosRobot(self, data):
         if("POS" in data and "dwm" not in data):
            data = data.strip("b'")
            data = data.strip("\r\n'")
            data = data.strip("POS,")
            data = data.split(',')
            self.pos_robot_x = float(data[0])
            self.pos_robot_y = float(data[1])
            self.pos_robot_z = float(data[2])
            self.pourcentage_precis = float(data[3])
         else:
            print("doesn't enter in condition")



    def fermer_port_radionavigation(self):
        self.ser.close()


    def demarrer_position(self):
        while self.doit_continuer: 
            self.obtenir_position_robot()
            sleep(1)
        


