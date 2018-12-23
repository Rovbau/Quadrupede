#! python
# -*- coding: utf-8 -*-
# Program berechnet 2xServo Winkel und 4xMotor_speed Robot
# Kurve  Links = +1 Rechts = -1
# Motors 1=VL 2=VR 3=HL 4=HR
# Servos Links = +90 Rechts= -90


from math import *
from MotorPwm import *
from Manuell import *
from ServoCont import *

class Motion():
    def __init__(self):
        self.ACHSDIST = 280.0
        self.BREITE = 350.0
        self.motor_pwm = MotorPWM()
        self.servo = Servo()

    def setMotion(self,steer,speed):
        self.steer, self.speed = steer, speed
        self.servo_l , self.servo_r = self.calc_ServoAngle(steer,speed)
        self.m1_speed, self.m2_speed, self.m3_speed, self.m4_speed = self.calc_Speed(self.steer,self.speed)

        if abs(self.speed) < 0.1:
            self.motor_pwm.setCommand(0,0,0,0)
            self.servo.set_servo_angle(0,0)
            return
        
        if self.speed > 0:
            self.motor_pwm.setCommand(self.m1_speed, self.m2_speed, self.m3_speed, self.m4_speed)
            self.servo.set_servo_angle(self.servo_l, self.servo_r)
            
        if self.speed < 0:
            self.m1_speed, self.m2_speed = self.m2_speed * (-1), self.m1_speed *(-1)
            self.m3_speed, self.m4_speed = self.m4_speed * (-1), self.m3_speed * (-1)
            self.servo_l , self.servo_r = self.servo_r * (-1) , self.servo_l * (-1)
            
            self.motor_pwm.setCommand(self.m1_speed, self.m2_speed, self.m3_speed, self.m4_speed)
            self.servo.set_servo_angle(self.servo_l, self.servo_r)

            
    def print_motion(self):
        print("%s %9.2f %9.2f" %("Motion: ",self.steer, self.speed))
        print("%s %7.2f %7.2f %7.2f %7.2f" %("MotorSpeed",self.m1_speed, self.m2_speed, self.m3_speed, self.m4_speed))
        print("%s %8.2f %8.2f" %("ServoAngle",self.servo_l , self.servo_r))
        print()
                   
    def angle_calc_servo(self,radii):
        servo_l = atan(self.ACHSDIST/(self.BREITE/2 + radii))
        servo_r = atan(self.ACHSDIST/(radii-self.BREITE/2))
        return(servo_l, servo_r)

    def calc_radii(self,steer,speed):
        steer = abs(steer)
        radii = (1.001 - steer) * 1000 + self.BREITE/2
        return(radii)

    def calc_ServoAngle(self, steer, speed):
        if abs(steer) < 0.1:
            return(0,0)

        if steer > 0:
            radii = self.calc_radii(steer,speed)
            servo_l, servo_r = self.angle_calc_servo(radii)
            servo_l, servo_r = servo_r * (-1), servo_l * (-1)
            return(degrees(servo_l) , degrees(servo_r))
            
        if steer < 0:
            radii = self.calc_radii(steer,speed)
            servo_l, servo_r = self.angle_calc_servo(radii)
            return(degrees(servo_l) , degrees(servo_r))

    def calc_Speed(self,steer,speed):       
        def helper_calculation(radii):            
            r_VL = radii + (self.BREITE/2)
            r_VR = radii - (self.BREITE/2)
            r_HL = sqrt(pow(self.ACHSDIST,2) + pow(radii + (self.BREITE/2),2))
            r_HR = sqrt(pow(self.ACHSDIST,2) + pow(radii - (self.BREITE/2),2))
            m1_speed = r_VL / radii
            m2_speed = r_VR / radii
            m3_speed = r_HL / radii
            m4_speed = r_HR / radii
            return(m1_speed, m2_speed, m3_speed, m4_speed)            
        
        if abs(steer) < 0.1:
            return(1,1,1,1)

        if steer > 0:
            radii = self.calc_radii(steer,speed)
            m1_speed, m2_speed, m3_speed, m4_speed = helper_calculation(radii)
            m1_speed, m2_speed, m3_speed, m4_speed = m2_speed, m1_speed, m4_speed, m3_speed
            return(m1_speed, m2_speed, m3_speed, m4_speed)
        
        if steer < 0:
            radii = self.calc_radii(steer,speed)
            m1_speed, m2_speed, m3_speed, m4_speed = helper_calculation(radii)            
            return(m1_speed, m2_speed, m3_speed, m4_speed)


if __name__ == "__main__":
    from Manuell import *

    
    manuell = Manuell()
    motion  = Motion()
    ThreadEncoder=Thread(target=manuell.runManuell,args=())
    ThreadEncoder.daemon=True
    ThreadEncoder.start()

    while True:
        steer, speed = manuell.getManuellCommand()
        motion.setMotion(steer, speed)
        motion.print_motion()
        sleep(1)






        

