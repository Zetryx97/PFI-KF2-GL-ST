from radionavigation import Radionavigation
from time import sleep
from moteur import Moteur



#radio_navig = Radionavigation()


#radio_navig.show_position_robot()
#sleep(1)
#radio_navig.fermer_port_radionavigation()
#sleep(1)

moteur_robot = Moteur()


moteur_robot .avancer(0.4)
sleep(2)
moteur_robot .freiner()
sleep(2)
moteur_robot .tourner_droite(0.7)
sleep(3)
