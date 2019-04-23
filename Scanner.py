#! python
# -*- coding: utf-8 -*-

from time import sleep
from Stepper import *
from Lidar import *
from math import *

class Scanner():
    def __init__(self):
        self.stepper = Stepper()
        self.lidar = Lidar()
        self.actual_steps = 0
        self.angle = 0
        self.direction = "CCW"
        self.scan_data = []
                
    def do_scan(self, step = 3, min_angle = -85, max_angle = 85):        
        while self.actual_steps < step:
            self.actual_steps += 1
            
            dist = self.lidar.get_distance()    # zero if LIDAR error
            if dist > 10:
                dx, dy = self.polar_to_kartesian(dist, self.angle)
                self.scan_data.append([dx,dy])

            if self.direction == "CCW":
                self.angle = round(self.angle + 1.8, 2)
                self.stepper.do_step(1)
            else:
                self.angle = round(self.angle - 1.8, 2)
                self.stepper.do_step(-1)
                
            if (self.angle >= max_angle):
                self.direction = "CW"
            if (self.angle <= min_angle):
                self.direction = "CCW"          
        self.actual_steps = 0

    def polar_to_kartesian(self, dist, winkel):
        """returns aus Dist und Winkel Dx,Dy"""
        dx=int((dist*cos(radians(winkel))))
        dy=int((dist*sin(radians(winkel))))
        return(dx,dy)

    def get_scan_data(self):
        data = self.scan_data
        self.scan_data = []
        return (data)
       
        
if __name__ == "__main__":
    scanner = Scanner()
    scanner.do_scan(step = 200)
    print("next")

