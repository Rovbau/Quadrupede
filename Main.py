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
from Transmit import *
from Planer import *


manuell = Manuell()
motion  = Motion()
battery = SMBUSBatt()
karte = Karte()
weggeber = Weggeber()
pathplaning = Pathplaning()
scanner = Scanner()
avoid = Avoid()
transmit = Transmit()
pumper = Pumper()
planer = Planer(avoid)

ThreadEncoder=Thread(target=manuell.runManuell,args=())
ThreadEncoder.daemon=True
ThreadEncoder.start()

theta_goal = 180
x_goal = 0
y_goal = 70
speed = 0.1
scans = []
steering_output = 0

scanner.scanner_reset()

while True:
    pumper.status_led("on")
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
    if speed == 1:
        scanner.do_scan(step=25)
        scan_data = scanner.get_scan_data()

        karte.updateObstacles(scan_data)
        obstacles = karte.getObstacles()
        
        avoid_steering, max_left, max_right = avoid.get_nearest_obst(x, y, pose, obstacles)
        steering_output = planer.set_modus(x, y, pose, avoid_steering, max_left, max_right)
        print(steering_output)
        avoided_obstacles = avoid.avoided_obst()
        #transmit.send_data(obstacles, avoided_obstacles, [[x,y]])
        #obstacles[0] = [x, y,pose]
        #scans.append(obstacles)
        #pickle_file = open("scanfile.p", "wb")
        #pickle.dump(scans, pickle_file)
        #pickle_file.close()

    #Manual
    steer, speed = manuell.getManuellCommand()
    steer = steering_output
    motion.stop(pumper.em_stop())
    motion.setMotion(steer, speed)
    if speed == 0:
        sleep(8)
    #print("---")
    pumper.status_led("off")
    sleep(0.3)
