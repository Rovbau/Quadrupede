#! python
# -*- coding: utf-8 -*-

from time import sleep
from Stepper import *
from Lidar import *

class Scanner():
    def __init__(self):
        self.stepper = Stepper()
        self.lidar = Lidar()
        self.actual_steps = 0
        self.angle = 0
        self.direction = "CCW"
                
    def do_scan(self, step = 3, min_angle = -50, max_angle = 50):        
        while self.actual_steps < step:
            self.actual_steps += 1     
            dist = self.lidar.get_distance()
            print(dist)
            sleep(0.01)

            if self.direction == "CCW":
                self.angle += 1
                self.stepper.do_step(1)
            else:
                self.angle -= 1
                self.stepper.do_step(-1)
                
            if (self.angle >= max_angle):
                self.direction = "CW"
            if (self.angle <= min_angle):
                self.direction = "CCW"          
        self.actual_steps = 0
       
        
if __name__ == "__main__":
    scanner = Scanner()
    scanner.do_scan(step = 600)
    print("next")
    scanner.do_scan(step = 600)
