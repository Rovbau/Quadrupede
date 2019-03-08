from Manuell import *
from Karte import *
from Motion import *
from Weggeber import *
from SMBUSBatt import *
from Pathplaning import *
from math import *


manuell = Manuell()
motion  = Motion()
battery = SMBUSBatt()
karte = Karte()
weggeber = Weggeber()
pathplaning = Pathplaning()

ThreadEncoder=Thread(target=manuell.runManuell,args=())
ThreadEncoder.daemon=True
ThreadEncoder.start()

theta_goal = 180
x_goal = 0
y_goal = 70
while True:

    if battery.get_relative_charge() < 30:
        print(5 *"BATTERY-EMPTY ")
        
    weggeber.update_weggeberpulse()
    deltaL, deltaR = weggeber.get_pulseLR()
    karte.updateRoboPos(deltaL, deltaR)
    x, y, pose = karte.getRoboPos()
    print(x, y,pose)

    soll_x, soll_y, soll_pose = pathplaning.move_to_pose(x, y, radians(pose), x_goal, y_goal, radians(theta_goal))
    print(soll_x, soll_y, soll_pose)
    steering_angle = pathplaning.get_steering_angle(radians(soll_pose), radians(pose))
    motion.setMotion(steering_angle, 0.2)
    print(steering_angle)
    print("---")
    sleep(0.3)
