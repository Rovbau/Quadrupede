#! python
# -*- coding: utf-8 -*-

from Avoid import *
from time import *


class Planer():
    def __init__(self, avoid):
        self.avoid = avoid
        self.wall_modus = False
        self.follow_left = False
        self.follow_right = False
        self.fixed_attraction = 0
        self.steering_output = 0
        self.goal_position = [3000,0]

    def set_modus(self, x, y, pose, avoid_steering, max_left, max_right):
        """Set Robot modus: wall or goal"""
        self.x = x
        self.y = y
        self.pose = pose
        self.avoid_steering = avoid_steering
        self.max_left = max_left
        self.max_right = max_right
   
        kurs_to_ziel = self.avoid.direction(x, y, self.goal_position[0], self.goal_position[1])
        self.kurs_diff = self.avoid.angle_diff(kurs_to_ziel, pose)
        
        if (abs(self.avoid_steering) > 0 and abs(self.kurs_diff) > 40) or self.wall_modus == True:
            self.modus_wall()
        elif self.wall_modus == False:
            self.modus_go_to_goal()
        return(self.steering_output)
        
    def modus_go_to_goal(self):
        print("modus_go_to_goal")
        self.steering_output =  self.avoid_steering

    def exit_wall_modus(self):
        dist = self.avoid.distance(self.x, self.y, self.goal_position[0], self.goal_position[1])
        if self.leaving_track_dist_to_goal - dist > 50:
            return(True)
        else:
            return(False)

    def modus_wall(self):
        if self.wall_modus == False:
            self.wall_modus = True
            self.leaving_track_dist_to_goal = self.avoid.distance(self.x, self.y, self.goal_position[0], self.goal_position[1])
            if self.kurs_diff <= 0:
                self.follow_left = False
                self.follow_right = True
                self.fixed_attraction = -0.5
            else:
                self.follow_left = True
                self.follow_right = False
                self.fixed_attraction = 0.5

        if self.follow_left:
            print("follow_left")
            self.steering_output = self.fixed_attraction + self.max_left
        if self.follow_right:
            print("follow_right")
            self.steering_output = self.fixed_attraction + self.max_right
        if self.exit_wall_modus():
            self.wall_modus = False
        return
    
if __name__ == "__main__":
    
    avoid = Avoid()
    avoid_steering, max_left, max_right = avoid.get_nearest_obst(0,0, 0, [[40,40],[100,10]])
    print(avoid.avoided_obst())
    planer = Planer(avoid)
    print(planer.set_modus(10, 10, 15, avoid_steering, max_left, max_right))
