# -*- coding: utf-8 -*-
#Weggeber
#Programm fragt Radencoder per I2c ab L/R.
#Ausgabe von Distanz und Abweichung der Räder

from time import sleep , time
import smbus
bus = smbus.SMBus(1)

class Weggeber():
    def __init__(self):
        """init Weggeber IC """
        self.CountL = 0
        self.CountR = 0
        self.last_time = time()

        #PIC Adresse
        self.addrweggeber=0x18
        _ = bus.read_byte_data(self.addrweggeber,0x01)  #Dummy read damit Counter null
        _ = bus.read_byte_data(self.addrweggeber,0x03)

        print("Init Weggeber")    

    def update_weggeberpulse(self):
        """Count pulse L und R und DistanzRad, loop"""
        #Get Weggeber counts and clear Register
        left_low = bus.read_byte_data(self.addrweggeber,0x01)  #Read PIC Register1 => CountsLowByte
        left_high = bus.read_byte_data(self.addrweggeber,0x02)  #read CountsHighByte
        left = (left_high << 8) + left_low
        if left > 32767:
            left = (65536 - left) * (-1)
        self.CountL = left
       
        right_low = bus.read_byte_data(self.addrweggeber,0x03)  #Read PIC Register1 => CountsLowByte
        right_high = bus.read_byte_data(self.addrweggeber,0x04)  #read CountsHighByte
        right = (right_high << 8) + right_low
        if right > 32767:
            right = (65536 - right) * (-1)
        self.CountR = right        

        return
    
    def clearWeggeberLR(self):
        """clears L / R Counts"""
        self.CountR=0
        self.CountL=0
        return
    
    def get_pulseLR(self):
        """Pulse an  L und R Rad"""
        return(self.CountL,self.CountR)

    def get_speedLR(self):
        """Anzahl Pulse je Sec"""
        diff = time() - self.last_time
        self.last_time = time()
        speedL = 1/diff * self.CountL
        speedR = 1/diff * self.CountR
        return(int(speedL), int(speedR))

if __name__ == "__main__":


    weggeber=Weggeber()

    while True:
        weggeber.update_weggeberpulse()
        print(weggeber.get_pulseLR())
        print(weggeber.get_speedLR())
        print("--------")
        sleep(1.21)
