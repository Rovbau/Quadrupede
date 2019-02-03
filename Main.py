from Manuell import *
from Karte import *
from Motion import *
from Weggeber import *
from SMBUSBatt import *


manuell = Manuell()
motion  = Motion()
battery = SMBUSBatt()
karte = Karte()
weggeber = Weggeber()

ThreadEncoder=Thread(target=manuell.runManuell,args=())
ThreadEncoder.daemon=True
ThreadEncoder.start()

while True:
    if battery.get_relative_charge() < 30:
        sleep(5)
        print(5 *"BATTERY-EMPTY ")
        
    weggeber.update_weggeberpulse()
    deltaL, deltaR = weggeber.get_pulseLR()
    karte.updateRoboPos(deltaL, deltaR, KompassCourse = None)
    print(karte.getRoboPos())
    
    steer, speed = manuell.getManuellCommand()
    motion.setMotion(steer, speed)
    motion.print_motion()
    
    sleep(1)
