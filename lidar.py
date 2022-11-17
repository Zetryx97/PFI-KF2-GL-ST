#Gabriel Lessard - Samy Tétrault
#PFI KF2

import PyLidar3




class Lidar:

    def __init__(self):
        self.port = "/dev/ttyUSB0"
        self.obj_lidar = PyLidar3.YdLidarX4(self.port)
        