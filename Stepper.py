#! python
# -*- coding: utf-8 -*-

from time import sleep
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

class Stepper():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.PINS_OUTPUT = [31,33,35,37]
        self.SEQ = [[1,1,0,0],
                    [0,1,1,0],
                    [0,0,1,1],
                    [1,0,0,1],
                    [1,1,0,0],
                    [0,1,1,0],
                    [0,0,1,1],
                    [1,0,0,1]]
        self.TOTAL_STEP = len(self.SEQ)
        self.step_counter = 0

        for pin in self.PINS_OUTPUT:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)
        self.set_step_output()
        print("Set Scanner to Zero position")
        sleep(3)

    def set_step_output(self):
        for pin in range(0, 4):
            x_pin = self.PINS_OUTPUT[pin]
            if self.SEQ[self.step_counter][pin]!=0:
                GPIO.output(x_pin, True)
                
            else:
                GPIO.output(x_pin, False)
                
    def do_step(self, step, speed = 0.01):
        for loop in range(0,abs(step)):
            if step > 0:
                self.step_counter += 1
            if step < 0:
                self.step_counter -= 1
                
            if (self.step_counter>=self.TOTAL_STEP):
                self.step_counter = 0
            if (self.step_counter<0):
                self.step_counter = self.TOTAL_STEP - 1
            self.set_step_output()
            sleep(speed)
        
        
if __name__ == "__main__":
    while True:
        stepper = Stepper()
        stepper.do_step(90)
        sleep (2)
        print("minus")
        stepper.do_step(-90)
        sleep (2) 
