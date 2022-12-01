from radionavigation import Radionavigation
from time import sleep
from moteur import Moteur



radio_navig = Radionavigation()


radio_navig.show_position_robot()
sleep(1)
radio_navig.fermer_port_radionavigation()
sleep(1)