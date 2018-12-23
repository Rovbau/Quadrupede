#! python
# -*- coding: utf-8 -*-
# Simple two DC motor PWM robot class

import time
import atexit

from Adafruit_MotorHAT import Adafruit_MotorHAT


class MotorPWM(object):
    def __init__(self, addr=0x60, left_id=1, right_id=2, left_trim=0, right_trim=0,
                 stop_at_exit=True):

        """Create an instance of the robot.  Can specify the following optional
        parameters:
         - addr: The I2C address of the motor HAT, default is 0x60.
         - left_id: The ID of the left motor, default is 1.
         - right_id: The ID of the right motor, default is 2.
         - left_trim: Amount to offset the speed of the left motor, can be positive
                      or negative and use useful for matching the speed of both
                      motors.  Default is 0.
         - right_trim: Amount to offset the speed of the right motor (see above).
         - stop_at_exit: Boolean to indicate if the motors should stop on program
                         exit.  Default is True (highly recommended to keep this
                         value to prevent damage to the bot on program crash!).
        """
        # Initialize motor HAT and left, right motor.
        self._mh = Adafruit_MotorHAT(addr)
        self._m1 = self._mh.getMotor(1)
        self._m2 = self._mh.getMotor(2)
        self._m3 = self._mh.getMotor(3)
        self._m4 = self._mh.getMotor(4)
        
        self._left_trim = left_trim
        self._right_trim = right_trim
        
        # Start with motors turned off.
        self._m1.run(Adafruit_MotorHAT.RELEASE)
        self._m2.run(Adafruit_MotorHAT.RELEASE)
        self._m3.run(Adafruit_MotorHAT.RELEASE)
        self._m4.run(Adafruit_MotorHAT.RELEASE)
        self.motor_backward = None
        
        # Configure all motors to stop at program exit if desired.
        if stop_at_exit:
            atexit.register(self.stop)

    def setCommand(self, m1_speed, m2_speed, m3_speed, m4_speed):
        """Set Motor1-4 Speed and Direction
        Input: [float -1.0 -> +1.0]
        Output [None]"""
 

        if m1_speed > 0:           
            self._m1.setSpeed(int(abs(m1_speed*200)))
            self._m2.setSpeed(int(abs(m2_speed*200)))
            self._m3.setSpeed(int(abs(m3_speed*200)))
            self._m4.setSpeed(int(abs(m4_speed*200)))
            self._m1.run(Adafruit_MotorHAT.FORWARD)
            self._m2.run(Adafruit_MotorHAT.FORWARD)         
            self._m3.run(Adafruit_MotorHAT.FORWARD)
            self._m4.run(Adafruit_MotorHAT.FORWARD)
            self.motor_backward = False
        else:
            self._m1.setSpeed(int(abs(m1_speed*200)))
            self._m2.setSpeed(int(abs(m2_speed*200)))
            self._m3.setSpeed(int(abs(m3_speed*200)))
            self._m4.setSpeed(int(abs(m4_speed*200)))
            self._m1.run(Adafruit_MotorHAT.BACKWARD)
            self._m2.run(Adafruit_MotorHAT.BACKWARD)         
            self._m3.run(Adafruit_MotorHAT.BACKWARD)
            self._m4.run(Adafruit_MotorHAT.BACKWARD)
            self.motor_backward = True

        if m1_speed and m2_speed and m3_speed and m4_speed == 0:
            self._m1.run(Adafruit_MotorHAT.RELEASE)
            self._m2.run(Adafruit_MotorHAT.RELEASE)         
            self._m3.run(Adafruit_MotorHAT.RELEASE)
            self._m4.run(Adafruit_MotorHAT.RELEASE)
 
    def motor_is_backward(self):
        """Returns TRUE wenn Motor retour"""
        return(self.motor_backward)

    
    def _left_speed(self, speed):
        """Set the speed of the left motor, taking into account its trim offset."""
        assert 0 <= speed <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        speed += self._left_trim
        speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._left.setSpeed(speed)

    def _right_speed(self, speed):
        """Set the speed of the right motor, taking into account its trim offset."""
        assert 0 <= speed <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        speed += self._right_trim
        speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._right.setSpeed(speed)

    def stop(self):
        """Stop all movement."""
        self._m1.run(Adafruit_MotorHAT.RELEASE)
        self._m2.run(Adafruit_MotorHAT.RELEASE)
        self._m3.run(Adafruit_MotorHAT.RELEASE)
        self._m4.run(Adafruit_MotorHAT.RELEASE)

    def forward(self, speed, seconds=None):
        """Move forward at the specified speed (0-255).  Will start moving
        forward and return unless a seconds value is specified, in which
        case the robot will move forward for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._left_speed(speed)
        self._right_speed(speed)
        self._left.run(Adafruit_MotorHAT.FORWARD)
        self._right.run(Adafruit_MotorHAT.FORWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def backward(self, speed, seconds=None):
        """Move backward at the specified speed (0-255).  Will start moving
        backward and return unless a seconds value is specified, in which
        case the robot will move backward for that amount of time and then stop.
        """
        # Set motor speed and move both backward.
        self._left_speed(speed)
        self._right_speed(speed)
        self._left.run(Adafruit_MotorHAT.BACKWARD)
        self._right.run(Adafruit_MotorHAT.BACKWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

            

            
### MAIN ###
    
if __name__ == "__main__":

    motor_pwm = MotorPWM()

    motor_pwm.setCommand(0,0,0,0)
    time.sleep(4)
    motor_pwm.setCommand(1,1,1,1) 
    time.sleep(4)
    motor_pwm.setCommand(0.1,0.2,0.3,0.8)
    time.sleep(8)

