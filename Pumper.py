#! python
# -*- coding: utf-8 -*-

from time import sleep
import RPi.GPIO as GPIO

class Pumper():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.pumper_L = 38
        self.pumper_R = 40
        GPIO.setup(self.pumper_L,GPIO.IN)
        GPIO.setup(self.pumper_R,GPIO.IN)

    def get_pumper_status(self):
        L = GPIO.input(self.pumper_L)
        R = GPIO.input(self.pumper_R)
        return(bool(L), bool(R))



if __name__ == "__main__":

    pumper = Pumper()
    print(pumper.get_pumper_status())
    sleep(1)
