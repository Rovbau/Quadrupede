#! python
# -*- coding: utf-8 -*-

from math import sqrt, exp, pi, degrees, atan2, atan, cos

class Avoid():
    def __init__(self):
        self.TRESHOLD = 0.5
        self.MAX_OBST_OBSERV = 200
        self.obst_fifo = []
        self.colision_obst = []

    def get_nearest_obst(self, robo_pos_x, robo_pos_y, pose, obstacles):
        self.robo_pos_x = robo_pos_x
        self.robo_pos_y = robo_pos_y
        self.pose = pose
        self.max_importance = 0
        self.obst_fifo.extend(obstacles)
        self.limit_fifo_lengh()
        self.colision_obst = self.colision_analysis(obstacles)
       
        for obstacle in self.colision_obst:
            dist = sqrt(pow(self.robo_pos_x - obstacle[0],2) + pow(self.robo_pos_y - obstacle[1],2))
            force = self.calc_force(dist)
            importance = force * cos(obstacle[2])
            if abs(importance) > self.TRESHOLD:
                if abs(importance) > self.max_importance:
                   self.max_importance =  importance
        return(self.max_importance)

    def colision_analysis(self, obstacles):
        self.colision_obst = []
        for obstacle in obstacles:
            kurs_to_obst = self.direction(self.robo_pos_x, self.robo_pos_y, obstacle[0], obstacle[1])
            kurs_diff = self.angle_diff(self.pose, kurs_to_obst)
            if  abs(kurs_diff) < 50:
                self.colision_obst.append([obstacle[0], obstacle[1], kurs_diff])
        return (self.colision_obst)

    def direction(self, x1, y1, x2, y2):
        dx, dy = (x2 - x1, y2 - y1)
        return (degrees(atan2(dy,dx)))
        
    def limit_fifo_lengh(self):        
        if len(self.obst_fifo) > self.MAX_OBST_OBSERV:
            len_fifo = len(self.obst_fifo) - self.MAX_OBST_OBSERV 
            del self.obst_fifo[:len_fifo]

    def calc_force(self, dist):
        avoid_force = exp(-(dist-60)*0.05)
        return(avoid_force)

    def angle_diff(self, soll, ist):
        """get de differenz between two angles"""
        angle = (soll-ist)
        if angle > 180:
            angle = 360 - angle
        if angle < -180:
            angle = 360 + angle
        return(angle)


if __name__ == "__main__":
    avoid = Avoid()
    robo_pos_x = 0
    robo_pos_y = 0
    pose       = 0
    obstacles = [[50,50],[50,-50], [200,300]]

    avoid.get_nearest_obst(robo_pos_x, robo_pos_y, pose, obstacles)




