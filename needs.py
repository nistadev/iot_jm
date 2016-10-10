#!/usr/bin/python3
"""
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' Components que necessitarem a tots els programes, he fet aquest fitxer   '
' per a centralitzar-ho tot i aixi escric menys codi a cada programa.      '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
"""

import RPi.GPIO as GPIO

#Variables globals
BUTTON1 = 6
BUTTON2 = 5
BUTTON3 = 25
BUTTON4 = 24
LED1 = 23
LED2 = 18
LED3 = 17

#Funcions
def inicialitza():
    """ Funcio inicialitza els components de GPIO """
    GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED1, GPIO.OUT)
    GPIO.setup(LED2, GPIO.OUT)
    GPIO.setup(LED3, GPIO.OUT)

