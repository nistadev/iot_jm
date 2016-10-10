#!/usr/bin/python3

#--------------------------------------------------------------------------#
# Components que necessitarem a tots els programes, he fet aquest fitxer   #
# per a centralitzar-ho tot i aixi escric menys codi a cada programa.      #
#--------------------------------------------------------------------------#


import RPi.GPIO as GPIO
import time

#Constants i variables
BUTTON1 = 6
BUTTON2 = 5
BUTTON3 = 25
BUTTON4 = 24
LED1 = 23
LED2 = 18
LED3 = 17
SEGONS = 5
seconds = 0.5
led_1 = False
led_2 = False
led_3 = False
actiu = 0

#Funcions
def inicialitza():
    """ Funcio inicialitza els components de GPIO """
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED1, GPIO.OUT)
    GPIO.setup(LED2, GPIO.OUT)
    GPIO.setup(LED3, GPIO.OUT)

def ts(temps):
    """ Retorna una pausa del temps especificat en segons """
    return time.sleep(temps)

def program_running(number):
    """ Funcio que mostra de manera visual en el programa que ens trobem segons el parametre """
    global led_1, led_2, led_3
    if number == 0:
        print("\n### Esteu en el programa inicial ###\n")
        val = True
        for i in range(2):
            """ Encen i apaga els leds alhora, segons la variable val """
            GPIO.output(LED1, val)
            GPIO.output(LED2, val)
            GPIO.output(LED3, val)
            ts(2)
            if val:
                val = False
            elif not val:
                val = True

    elif number == 1:
        print("\n### Esteu en el programa d'enviament de dades ###\n")
        num = 0
        while (num < 8):
            """ Encen i apaga els leds un darrere l'altre """
            if (led_1 != True) and (led_2 != True) and (led_3 != True):
                led_1 = True
                GPIO.output(LED1, True)
                ts(.15)
            elif led_1 != False:
                led_1 = False
                GPIO.output(LED1, False)
                led_2 = True
                GPIO.output(LED2, True)
                ts(.15)
            elif led_2 != False:
                led_2 = False
                GPIO.output(LED2, False)
                led_3 = True
                GPIO.output(LED3, True)
                ts(.15)
            elif led_3 != False:
                led_3 = False
                GPIO.output(LED3, False)
                ts(.15)
            num += 1

    elif number == 2:
        print("\n### Esteu en el programa de fer proves ###\nUtilitzi els botons per a provar els diferents components.\n")
        val = True
        for i in range(6):
            """ Encen i apaga els leds segons la variable val """
            GPIO.output(LED1, val)
            GPIO.output(LED2, val)
            GPIO.output(LED3, val)
            ts(0.1)
            if val:
                val = False
            elif not val:
                val = True
