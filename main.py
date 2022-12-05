from radionavigation import Radionavigation
from moteur import Moteur
from time import sleep




#radio_navig = Radionavigation()


#radio_navig.show_position_robot()
#sleep(1)
#radio_navig.fermer_port_radionavigation()
#sleep(1)
moteur = Moteur()
radio = Radionavigation()
radio.show_position_robot()
sleep(5)
radio.show_position_robot()
sleep(5)
radio.show_position_robot()
sleep(5)
radio.show_position_robot()
sleep(5)
radio.show_position_robot()
sleep(5)
radio.show_position_robot()
radio.doit_continuer = False
print("fini!")

