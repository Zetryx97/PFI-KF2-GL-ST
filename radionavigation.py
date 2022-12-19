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
        self.ser.write(b'\r\r') #commande shell
        sleep(1)
        self.ser.write(b'lep\n')#commande shell
        sleep(1)
        self.ser.close()
        self.pos_robot_x = 0
        self.pos_robot_y = 0
        self.pourcentage_precis = None
        self.doit_continuer = True


    def show_position_robot(self):
        self.ser.open()
        data = str(self.ser.readline().decode("utf-8"))
        self.ser.close()
        #Convert data
        self.updatePosRobot(data)
        

    def updatePosRobot(self, data):
        if("POS" in data and "dwm" not in data):
            data = data.strip("b'")
            data = data.replace('\r\n','')
            data = data.strip("'")
            data = data.strip("POS,")
            tab = data.split(',')
            self.pos_robot_x = float(tab[0])
            self.pos_robot_y = float(tab[1])
            self.pourcentage_precis = tab[3]
        else:
            self.pos_robot_x = 0
            self.pos_robot_y = 0
            self.pourcentage_precis = None

    def demarrer_position(self):
        while self.doit_continuer:
            sleep(0.5)
            self.show_position_robot()
            print(self.pos_robot_x)
            print(self.pos_robot_y)

if __name__ == "__main__":
    import threading

    radio = Radionavigation()
    th_radio = threading.Thread(target=radio.demarrer_position)
    th_radio.start()
    sleep(40)
    radio.doit_continuer = False
    print("fini!")


