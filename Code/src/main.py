"""
    Main.py
Programme de fonctionnement général

Cette version est hautement inspirer d'exemples sur internet, mais est optimiser
en objet je n'ai garder que le nécessaire pour la pédale multi-mod dans le cadre de
l'obtention de mon DEC technique

Faire référence aux documents suivant pour le fonctionnement complet:
    LCD_Lib.py
    Functions.py

--Auteur     : Colin Boulé
--Revision   : 001
--First Rev. : 2023/01/30
--Last Rev.  : 2023/01/30

"""
# ================================================================================================== #
# -- DEPENDENCIES
import machine, time, utime
from machine import Pin
import LCD_Lib
from LCD_Lib import Lcd2004
import Functions
from Functions import menu, i2c_controls

# ================================================================================================== #

# ================================================================================================== #
# -- STRINGS
Menu       = [['?____Modulations____WMod 2    mod2 wMod 1    mod1 ZMod 3    mod3 '],
              ['?___Peripheriques___WSortie   zwEntree   y                    '], 
              
              ['_____Distortion_____W______             wIntensite     Bris Zretour             ',  
               '________Fuzz________W______             wIntensite     x/10Zretour             '],
              
              ['______Tremolo_______WPortee        y/10wFrequence     x/10Zretour             ',  
               '______Vibrato_______W______             wFrequence     x/10Zretour             '],
              
              ['_______Chorus_______W_______            w______             Zretour             ',  
               '___Reverberation____W______             wDelais        x/10Zretour             ']]

# -- VARIABLES
cursor = 1
Output = 0
Input  = 0
MOD1   = 0
MOD2   = 0
MOD3   = 0
ajustements = [[[0,0],[0,0]],
               [[0,0],[0,0]],
               [[0,0],[0,0]]]
menuX  = 0
menuY  = 0
presentPage = Menu[menuX][menuY]

# -- OBJECTS
up   = Pin(14, Pin.IN, Pin.PULL_UP) #button
down = Pin(12, Pin.IN, Pin.PULL_UP) #button
ok   = Pin(13, Pin.IN, Pin.PULL_UP) #button
left = Pin(11, Pin.IN, Pin.PULL_UP) #button
right= Pin(15, Pin.IN, Pin.PULL_UP) #button
LCD  = Lcd2004(7,6,5,4,3,2)         #screen
LCD.__init__(7,6,5,4,3,2)           #screen
interface = menu(LCD, presentPage)
controls = i2c_controls(26,27,16,17)
controls.__init__(26,27,16,17)
controls.chooseMODS(MOD1,MOD2,MOD3,Output, Input)


# - INTERUPT (FLAGS/OTHERS)
okFlag        = 0
rightFlag     = 0
leftFlag      = 0
refreshFlag   = 1
debounce_time = 0

# ================================================================================================== #

# ================================================================================================== #
# -- LAZY FUNCTIONS
def switchPage(condition, option1, option2, option3):
    global refreshFlag,cursor,presentPage, interface
    if(presentPage == condition and refreshFlag == 0):
            presentPage = interface.choosePage(option1, option2, option3, cursor)
            refreshFlag = 1

def increment(variable, maximum):
    if variable < maximum:
        variable += 1
    return variable
        
def decrement(variable, minimum):
    if variable > minimum:
        variable -= 1
    return variable

def transform(data, maximum):
    return int((data*maximum)/10)

# ================================================================================================== #

# ================================================================================================== #
# -- CALLBACKS
def callbackUP(up):
    global refreshFlag, debounce_time, cursor
    if (time.ticks_ms()-debounce_time) > 175:
        debounce_time=time.ticks_ms()
        cursor = decrement(cursor, 0)
        refreshFlag = 1

def callbackOK(ok):
    global okFlag, refreshFlag, debounce_time, cursor, menuStep,menuX,menuY
    if (time.ticks_ms()-debounce_time) > 175:
        debounce_time=time.ticks_ms()
        if(menuX > 1 and cursor == 3):
            menuX = 0
            menuY = 0
            refreshFlag = 1
            
        if(presentPage == Menu[0][0] and cursor > 0):
            if (cursor == 1):
                if(MOD1 != 0):
                    menuX = 2
                    menuY = MOD1 - 1
            elif (cursor == 2):
                if(MOD2 != 0):
                    menuX = 3
                    menuY = MOD2 - 1
                    
            elif (cursor == 3):
                if(MOD3 != 0):
                    menuX = 4
                    menuY = MOD3 - 1
            refreshFlag = 1
        print(str(menuY) +" "+ str(menuX))
                

def callbackDOWN(down):
    global refreshFlag, debounce_time, cursor
    if (time.ticks_ms()-debounce_time) > 175:
        debounce_time=time.ticks_ms()
        cursor = increment(cursor,3)
        refreshFlag = 1
            
def callbackRIGHT(right):
    global refreshFlag,rightFlag, debounce_time, cursor, menuStep, menuX,Input, Output
    if (time.ticks_ms()-debounce_time) > 175:
        debounce_time=time.ticks_ms()
        if(menuX > 0 and cursor == 0):
            menuX-=1
            refreshFlag = 1
        else:
            rightFlag = 1

def callbackLEFT(left):
    global refreshFlag,leftFlag, debounce_time, cursor, menuX, menuY, presentPage, Input, Output
    if (time.ticks_ms()-debounce_time) > 175:
        debounce_time=time.ticks_ms()
        if (menuX == 0 and cursor == 0):
            menuX+=1
            refreshFlag = 1
        else:
            leftFlag = 1

up.irq(trigger=Pin.IRQ_FALLING, handler=callbackUP)
ok.irq(trigger=Pin.IRQ_FALLING, handler=callbackOK)
down.irq(trigger=Pin.IRQ_FALLING, handler=callbackDOWN)
left.irq(trigger=Pin.IRQ_FALLING, handler=callbackLEFT)
right.irq(trigger=Pin.IRQ_FALLING, handler=callbackRIGHT)
# ================================================================================================== #


# ================================================================================================== #
# -- APPLICATION
while(True):
    #================================================================================ REFRESH flag (LCD print) 
    if(refreshFlag == 1):
        presentPage = Menu[menuX][menuY]
        if(presentPage == Menu[0][0]):
            interface.printModulationPage(presentPage, cursor, MOD1, MOD2, MOD3)
        elif(presentPage == Menu[1][0]):
            interface.printPeripheralPage(presentPage,cursor, Input, Output)
        elif(menuX>1):
            interface.printSettingPage(presentPage, cursor, ajustements[menuX-2][menuY][0], ajustements[menuX-2][menuY][1]);
        else:
            interface.printMenuPage(presentPage, cursor)
        refreshFlag = 0
        #================================================================================
        
        
    #================================================================================ LEFT button   
    if (leftFlag ==1):
        leftFlag = 0
        
        if (presentPage==Menu[1][0]):
            if(cursor == 1):
                Input = increment(Input, 1)
            elif(cursor == 2):
                Output = increment(Output, 1)
            controls.chooseMODS(MOD1,MOD2,MOD3,Output, Input)
                
        elif (presentPage==Menu[0][0]):
            if(cursor == 1):
                MOD1 = increment(MOD1, 2)
            elif(cursor == 2):
                MOD2 = increment(MOD2, 2)
            elif(cursor == 3):
                MOD3 = increment(MOD3, 2)
            controls.chooseMODS(MOD1,MOD2,MOD3,Output, Input)
                
        elif (presentPage==Menu[2][0]):
            if (cursor == 1):
                ajustements[0][0][0] = increment(ajustements[0][0][0], 9)
                data = transform((ajustements[0][0][0])+1,255)
                controls.setDistortion(data)
            
        elif (presentPage==Menu[2][1]):
            if (cursor == 1):
                ajustements[0][1][0] = increment(ajustements[0][1][0], 9)
                data = transform((ajustements[0][1][0])+1, 63) 
                controls.setFuzz(data)
        
        elif (presentPage==Menu[3][0]):
            if (cursor == 1):
                ajustements[1][0][0] = increment(ajustements[1][0][0], 9)
            if (cursor == 2):
                ajustements[1][0][1] = increment(ajustements[1][0][1], 9)
            data = int(transform((ajustements[1][0][0])+1,63))
            data2 = int(transform((ajustements[1][0][1])+1,63))
            controls.setTremolo(data, data2)
            
        elif (presentPage==Menu[3][1]):
            if (cursor == 1):
                ajustements[1][1][0] = increment(ajustements[1][1][0], 9)
                data = transform((ajustements[1][1][0])+1,63)
                controls.setVibrato(data)
        
        elif (presentPage==Menu[4][0]):
            if (cursor == 1):
                ajustements[2][0][0] = increment(ajustements[2][0][0], 9)
            
        elif (presentPage==Menu[4][1]):
            if (cursor == 1):
                ajustements[2][1][0] = increment(ajustements[2][1][0], 9)
                data = transform((ajustements[2][1][0])+1,63)
                controls.setReverb(data)
                
        refreshFlag = 1
        #================================================================================
        
        
    #================================================================================ RIGHT button 
    if (rightFlag == 1):
        rightFlag = 0

        if (presentPage==Menu[1][0]):
            if(cursor == 1):
                Input = decrement(Input, 0)
            elif(cursor == 2):
                Output = decrement(Output, 0)
            controls.chooseMODS(MOD1,MOD2,MOD3,Output, Input)
  
        elif (presentPage==Menu[0][0]):
            if(cursor == 1):
                MOD1 = decrement(MOD1, 0)
            elif(cursor == 2):
                MOD2 = decrement(MOD2, 0)
            elif(cursor == 3):
                MOD3 = decrement(MOD3, 0)
            controls.chooseMODS(MOD1,MOD2,MOD3,Output, Input)
                
        elif (presentPage==Menu[2][0]):
            if (cursor == 1):
                ajustements[0][0][0] = decrement(ajustements[0][0][0], 0)
                data = int(transform((ajustements[0][0][0])+1,255))
                controls.setDistortion(data)
            
        elif (presentPage==Menu[2][1]):
            if (cursor == 1):
                ajustements[0][1][0] = decrement(ajustements[0][1][0], 0)
                data = int(transform((ajustements[0][1][0])+1,63))
                controls.setFuzz(data)
        
        elif (presentPage==Menu[3][0]):
            if (cursor == 1):
                ajustements[1][0][0] = decrement(ajustements[1][0][0], 0)
            if (cursor == 2):
                ajustements[1][0][1] = decrement(ajustements[1][0][1], 0)
            data = int(transform((ajustements[1][0][0])+1,63))
            data2 = int(transform((ajustements[1][0][1])+1,63))
            controls.setTremolo(data, data2)
            
        elif (presentPage==Menu[3][1]):
            if (cursor == 1):
                ajustements[1][1][0] = decrement(ajustements[1][1][0], 0)
                data = int(transform((ajustements[1][1][0])+1,63))
                controls.setVibrato(data)
        
        elif (presentPage==Menu[4][0]):
            if (cursor == 1):
                ajustements[2][0][0] = decrement(ajustements[2][0][0], 0)
            
        elif (presentPage==Menu[4][1]):
            if (cursor == 1):
                ajustements[2][1][0] = decrement(ajustements[2][1][0], 0)
                data = int(transform((ajustements[2][1][0])+1,63))
                controls.setReverb(data)
        
        refreshFlag = 1
        #================================================================================
        
     
# ================================================================================================== #



