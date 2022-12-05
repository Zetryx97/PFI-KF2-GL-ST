#Gabriel Lessard - Samy Tétrault
#PFI KF2

import serial
from time import sleep


class Radionavigation:
    def __init__(self):
        self.ser = serial.Serial()
        self.ser.port = '/dev/ttyACM0'
        self.ser.baudrate = 115200
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 1
        self.ser.open()
        self.pos_robot_x = None
        self.pos_robot_y = None
        self.pourcentage_precis = None
        self.doit_continuer = True


    def show_position_robot(self):
        self.ser.write(b'\r\r') #commande shell
        sleep(1)
        self.ser.write(b'lep\n')#commande shell
        data = str(self.ser.readline().decode("utf-8"))
        sleep(1)
        #Convert data
        self.updatePosRobot(data)

        print("POS: ")
        print(self.pos_robot_x)
        print(self.pos_robot_y)
        print(self.pourcentage_precis)
        

    def updatePosRobot(self, data):
         if("POS" in data and "dwm" not in data):
            data = data.strip("b'")
            data = data.strip("\r\n'")
            data = data.strip("POS,")
            data = data.split(',')
            self.pos_robot_x = float(data[0])
            self.pos_robot_y = float(data[1])
            self.pourcentage_precis = float(data[3])
         else:
            print("doesn't enter in condition")
            self.pos_robot_x = None
            self.pos_robot_y = None
            self.pourcentage_precis = None

    def demarrer_position(self):
        while self.doit_continuer: 
            sleep(1)
            self.show_position_robot()
        


