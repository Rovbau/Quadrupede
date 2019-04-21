from Manuell import *
from Karte import *
from Motion import *
from Weggeber import *
from SMBUSBatt import *
from Pathplaning import *
from Scanner import *
from math import *
import pickle
from Avoid import *


manuell = Manuell()
motion  = Motion()
battery = SMBUSBatt()
karte = Karte()
weggeber = Weggeber()
pathplaning = Pathplaning()
scanner = Scanner()
avoid = Avoid()

ThreadEncoder=Thread(target=manuell.runManuell,args=())
ThreadEncoder.daemon=True
ThreadEncoder.start()

theta_goal = 180
x_goal = 0
y_goal = 70
speed = 0.1
scans = []

while True:
    
    if battery.get_relative_charge() < 30:
        print(3 *"BATTERY-EMPTY ")

    #Position        
    weggeber.update_weggeberpulse()
    deltaL, deltaR = weggeber.get_pulseLR()
    karte.updateRoboPos(deltaL, deltaR)
    x, y, pose = karte.getRoboPos()
    print(x, y,pose)

##    soll_x, soll_y, soll_pose = pathplaning.move_to_pose(x, y, radians(pose), x_goal, y_goal, radians(theta_goal))
##    print(soll_x, soll_y, soll_pose)
##    steering_angle = pathplaning.get_steering_angle(radians(soll_pose), radians(pose))
##    motion.setMotion(steering_angle, 0.2)
##    print(steering_angle)

    #Scan
    if speed == 0:
        scanner.do_scan(step=25)
        #motion.setMotion(0,0)
        scan_data = scanner.get_scan_data()
        karte.updateObstacles(scan_data)
        pickle_file = open("scanfile.p", "wb")
        obstacles = karte.getObstacles()

        max_importance = avoid.get_nearest_obst(x, y, pose, obstacles)
        print("max_importance: " +str(max_importance))

        
        obstacles[0] = [x, y,pose]
        scans.append(obstacles)
        pickle.dump(scans, pickle_file)
        pickle_file.close()

    #Manual
    steer, speed = manuell.getManuellCommand()
    motion.setMotion(steer, speed)
    print("---")
    sleep(3.3)
