"""
    Functions.py
Librairie personnel pour le fonctionnement de la pédale multi-mod dans le cadre de
l'obtention de mon DEC technique

Ce document contient mes fonctions afin d'alléger mon code principal, il contient
tout et rien. 

--Auteur     : Colin Boulé
--Revision   : 001
--First Rev. : 2023/01/30
--Last Rev.  : 2023/01/30

"""
#==========================================================================================#
#                                ---- DEPENDENCIES ----                                    #
import machine
from machine import Pin
import LCD_Lib
from LCD_Lib import Lcd2004
import time
import utime

#==========================================================================================#
#                                 ---- REFERENCES ----                                     #
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line
LCD_CLR   = 0x01  # DB0: clear display 
LCD_HOME = 0x02
LCD_MOVE_RIGHT = 0x04
LCD_ON_BLINK = 0x01
LCD_ON_CURSOR = 0x02

ADDR_PHASE1_POT_200K = 44
ADDR_PHASE1_POT_1K = 76

ADDR_PHASE2_POT_100k_1 = 47
ADDR_PHASE2_POT_100k_2 = 46
ADDR_PHASE2_POT_100k_3 = 47

ADDR_PHASE3_POT_50k_1 = 76

ADDR_IO_EXPANDER = 33

#==========================================================================================#
#                                    ---- DEFINITIONS ----                                 #

def _init_Buttons(up, down, ok):
    up   = Pin(13, Pin.IN, Pin.PULL_UP)
    down = Pin(14, Pin.IN, Pin.PULL_UP)
    ok   = Pin(15, Pin.IN, Pin.PULL_UP)

#==========================================================================================#
    

#==========================================================================================#
#                             ---- LCD SCREEN FUNCTIONS ----                               #
class menu():
    def __init__(self, screen,string):
        self.screen = screen
        self.string = string
        self.Input  = ["Jack      ","Aux       ","Conn      "]
        self.Output = ["Jack      ","Aux       ","Conn      "]
        self.MOD1   = ["Rien      ","Distortion","Fuzz      "]
        self.MOD2   = ["Rien      ","Tremolo   ","Vibrato   "]
        self.MOD3   = ["Rien      ","Chorus     ","Reverb   "]
        self.grades = [" 1"," 2"," 3"," 4"," 5"," 6"," 7"," 8"," 9","10",]
        
    def printPage(self, string):
        self.screen.setUpLCD()
        self.screen.writeCmd(LCD_LINE_1)
        self.screen.writeStr(string)

    def printMenuPage(self, string, cursor):
        if cursor == 1:
            self.string =      string.replace("w",">")
            self.string = self.string.replace("W"," ")
            self.string = self.string.replace("Z"," ")
            self.string = self.string.replace("?"," ")
        elif cursor == 2:
            self.string =      string.replace("w"," ")
            self.string = self.string.replace("W",">")
            self.string = self.string.replace("Z"," ")
            self.string = self.string.replace("?"," ")
        elif cursor == 3:
            self.string =      string.replace("w"," ")
            self.string = self.string.replace("W"," ")
            self.string = self.string.replace("Z",">")
            self.string = self.string.replace("?"," ")
        elif cursor == 0:
            self.string =      string.replace("w"," ")
            self.string = self.string.replace("W"," ")
            self.string = self.string.replace("Z"," ")
            self.string = self.string.replace("?",">")
        
        self.printPage(self.string)
        
    def printPeripheralPage(self, string, cursor, Input, Output):
        self.string =      string.replace("y",self.Input[Input])
        self.string = self.string.replace("z",self.Output[Output])
        self.printMenuPage(self.string, cursor)
        
    def printModulationPage(self, string, cursor, MOD1, MOD2, MOD3):
        self.string =      string.replace("mod1 ",self.MOD1[MOD1])
        self.string = self.string.replace("mod2 ",self.MOD2[MOD2])
        self.string = self.string.replace("mod3 ",self.MOD3[MOD3])
        self.printMenuPage(self.string, cursor)
        
    def printSettingPage(self, string, cursor, value1, value2):
        self.string =      string.replace("x",self.grades[value1])
        self.string = self.string.replace("y",self.grades[value2])
        self.printMenuPage(self.string, cursor)
        
    def choosePage(self, option1, option2, option3, cursor):
        if cursor == 1:
            self.string = option1
        elif cursor == 2:
            self.tring = option2
        elif cursor == 3:
            self.string = option3
        
        printPage(self.string, self.screen)
        
#==========================================================================================#
        
        
#==========================================================================================#
#                           ---- CONTROLABLE COMPONENTS ----                               #

class i2c_controls:
    def __init__(self, SDA1, SCL1, SDA2, SCL2):
        self.i2c1 = machine.I2C(1,sda = Pin(SDA1), scl = Pin(SCL1), freq = 400000)
        self.i2c2 = machine.I2C(0,sda = Pin(SDA2), scl = Pin(SCL2), freq = 400000)

        
    def setIOEXP(self, P1_output,P0_output):
        data_frame = bytearray([0x07, 0x00])
        self.i2c2.writeto(ADDR_IO_EXPANDER, data_frame)
        data_frame = bytearray([0x03, P1_output])
        self.i2c2.writeto(ADDR_IO_EXPANDER, data_frame)
        
        data_frame = bytearray([0x06, 0x00])
        self.i2c2.writeto(ADDR_IO_EXPANDER, data_frame)
        data_frame = bytearray([0x02, P0_output])
        self.i2c2.writeto(ADDR_IO_EXPANDER, data_frame)
    
        
    def chooseMODS(self, MOD1,MOD2,MOD3, OUT, IN):
        P0 = 0x00
        P1 = 0x00

        if MOD1 == 0: P0 = P0 + 0x04
        elif MOD1 == 1: P0 = P0 + 0x02
        elif MOD1 == 2: P0 = P0 + 0x01
        
        if MOD2 == 0: P0 = P0 + 0x20
        elif MOD2 == 1: P0 = P0 + 0x10
        elif MOD2 == 2: P0 = P0 + 0x08
        
        if MOD3 == 0: P0 = P0 + 0x80
        elif MOD3 == 1: P0 = P0 + 0x40
        elif MOD3 == 2: P1 = P1 + 0x01
        
        if OUT == 0: P1 = P1 + 0x80
        elif OUT == 1: P1 = P1 + 0x20
        elif OUT == 2: P1 = P1 + 0x40
    
        if IN == 0: P1 = P1 + 0x10
        elif IN == 1: P1 = P1 + 0x08
        elif IN == 2: P1 = P1 + 0x04
        
        self.setIOEXP(P1, P0)
    
    
    def setDistortion(self,msg):
        data_frame = bytearray([0x00, msg])
        self.i2c1.writeto(ADDR_PHASE1_POT_200K, data_frame)
        
    def setFuzz(self, msg):
        data_frame = bytearray([0x00, msg])
        self.i2c1.writeto(ADDR_PHASE1_POT_1K, data_frame)
        
        
    def setVibrato(self,msg):
        data_frame = bytearray([msg])
        self.i2c2.writeto_mem(ADDR_PHASE2_POT_100k_1,0x00, data_frame)
    
    def setTremolo(self,freq, depth):
        data_frame = bytearray([0x00, freq])
        self.i2c1.writeto(ADDR_PHASE2_POT_100k_2, data_frame)
        data_frame = bytearray([0x00, depth])
        self.i2c1.writeto(ADDR_PHASE2_POT_100k_3, data_frame)
        
        
    def setReverb(self,msg):
        data_frame = bytearray([0x00, msg])
        self.i2c2.writeto(ADDR_PHASE3_POT_50k_1, data_frame)

        
#==========================================================================================#


    

    
    
    
    