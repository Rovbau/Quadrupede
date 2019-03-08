#! python
# -*- coding: utf-8 -*-

from math import *
import numpy as np
from random import random


class Pathplaning():
    def __init__(self):       
        # simulation parameters
        print("Init Pathplaning")
        self.KP_RHO = 5
        self.KP_ALPHA = 20
        self.KP_BETA = -7
        self.DTIME = 0.05

    def move_to_pose(self, x_start, y_start, theta_start, x_goal, y_goal, theta_goal):
        """
        rho is the distance between the robot and the goal position
        alpha is the angle to the goal relative to the heading of the robot
        beta is the angle between the robot's position and the goal position plus the goal angle

        Kp_rho*rho and Kp_alpha*alpha drive the robot along a line towards the goal
        Kp_beta*beta rotates the line so that it is parallel to the goal angle
        """
        x = x_start
        y = y_start
        theta = theta_start

        x_diff = x_goal - x
        y_diff = y_goal - y

        rho = sqrt(x_diff**2 + y_diff**2)

        #while rho > 0.05:
        x_diff = x_goal - x
        y_diff = y_goal - y

        # Restrict alpha and beta (angle differences) to the range
        # [-pi, pi] to prevent unstable behavior e.g. difference going
        # from 0 rad to 2*pi rad with slight turn

        rho = sqrt(x_diff**2 + y_diff**2)
        alpha = (atan2(y_diff, x_diff)
                 - theta + pi) % (2 * pi) - pi
        beta = (theta_goal - theta - alpha + pi) % (2 * pi) - pi

        v = self.KP_RHO * rho
        w = self.KP_ALPHA * alpha + self.KP_BETA * beta

        if alpha > pi / 2 or alpha < -pi / 2:
            v = -v

        theta = theta + w * self.DTIME
        x = x + v * cos(theta) * self.DTIME
        y = y + v * sin(theta) * self.DTIME
        return(round(x, 2), round(y, 2), round((degrees(theta)), 2))


    def get_steering_angle(self, soll, ist):
        """get de differenz between two angles"""
        angle = (soll-ist)
        if angle > 180:
            angle = 2*pi - angle
        if angle < -180:
            angle = 2*pi + angle
        return(angle)

if __name__ == '__main__':

    pathplaning = Pathplaning()
    x_start = 10
    y_start = 10
    theta_start = 0.0
    x_goal = 20
    y_goal = 20
    theta_goal = 1.5
    print("Initial x: %.2f m\nInitial y: %.2f m\nInitial theta: %.2f rad\n" %
          (x_start, y_start, theta_start))
    print("Goal x: %.2f m\nGoal y: %.2f m\nGoal theta: %.2f rad\n" %
          (x_goal, y_goal, theta_goal))
    pathplaning.move_to_pose(x_start, y_start, theta_start, x_goal, y_goal, theta_goal)



    
