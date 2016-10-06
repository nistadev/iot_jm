#!/usr/bin/python3

""" 
---------------------------------------------------------------
| Script per fer tests amb el hardware instalat de la RaspIoT |
---------------------------------------------------------------
"""

#Llibreries
import sys, os, time
import RPi.GPIO as GPIO
import Adafruit_DHT as DHT
from valorlux import *

#Inicialitzacions previes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Variables Globals
BUTTON1 = 6
BUTTON2 = 5
BUTTON3 = 25
BUTTON4 = 24
LED1 = 23
LED2 = 18
LED3 = 17
DHT_TYPE = DHT.DHT22
DHT_PIN = 13 
apretat = 0
seconds = 0.5
actiu = 0
led_1 = False
led_2 = False
led_3 = False

#Inicialitacio components GPIO
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)

#Variables objecte
button_1 = GPIO.input(BUTTON1)
button_2 = GPIO.input(BUTTON2)
button_3 = GPIO.input(BUTTON3)
button_4 = GPIO.input(BUTTON4)
tsl = TSL2561()

# Funcions
def ts(temps):
    """ Retorna un temps d'espera basat en parametre del temps que agafem """
    return time.sleep(temps)

def primer():
    """ Funcio que ens diu que estem en aquest programa i que fa una senyal visual amb els leds per a saber-ho """

    print("\nEsteu en el programa de fer proves. Utilitzi els botons per a provar els diferents components.")

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

def gethyt():
    """ Guarda les dades llegides per el sensor de temperatura i humitat en les respectives variables globals """
    global hum, temp
    hum, temp = DHT.read(DHT_TYPE, DHT_PIN)


""" Inici del programa """

primer() # Executem la funcio d'inici abans d'entrar al loop

while True:
    """ --------------------------------------------------------------
        Loop que ens permetra controloar el dispositiu amb els botons.
          1. Ens mostrara els lux.
          2. Ens mostrara la temperatura i la humitat.
          3. Encendra els leds un per un.
          4. Surt del programa.
        --------------------------------------------------------------
    """

    # Variable per determinar si estem en una de les accions del boto.
    # Aixo evitara tenir accions simultanies i per tant evitara els problemes que deriven d'aixo.
    testing = False 

    while (button_4 != actiu):
        """ Executa el codi mentre el boto 4 no esta actiu """
        button_1 = GPIO.input(BUTTON1) # Actualitzem els valors dels botons a cada volta.
        button_2 = GPIO.input(BUTTON2)
        button_3 = GPIO.input(BUTTON3)
        button_4 = GPIO.input(BUTTON4)

        # Comprovem si l'usuari ha apretat algun boto i executem les accions en cas afirmatiu.
        if button_1 == actiu and not testing:
            testing = True
            ts(seconds)
            if tsl.foundSensor():
                tsl.setGain(tsl.GAIN_16X); #Pot ser 0X o 16X
                tsl.setTiming(tsl.INTEGRATIONTIME_13MS)
                full = tsl.getLuminosity(tsl.FULLSPECTRUM)
                infrared = tsl.getLuminosity(tsl.INFRARED)
                print("Lux: {}".format(tsl.calculateLux(full, infrared)))
            else:
                print("Hi ha sensor?")
            testing = False
	
        if button_2 == actiu and not testing:
            testing = True
            ts(seconds)
            gethyt()
            if hum != None and temp != None:
                print("Temperatura: {0:0.1f}".format(temp))
                print("Humiditat: {0:0.1f}".format(hum))
                testing = False
            else:
                if pases < 3:
                    gethyt()
                else:
                    testing = False
	
        if button_3 == actiu:
            ts(seconds)
            # Comprovem en quina fase de l'accio es troba per determinar si encenem/apaguem un led
            if (led_1 != True) and (led_2 != True) and (led_3 != True):
                led_1 = True
                GPIO.output(LED1, True)

            elif led_1 != False:
                led_1 = False
                GPIO.output(LED1, False)
                led_2 = True
                GPIO.output(LED2, True)

            elif led_2 != False:
                led_2 = False
                GPIO.output(LED2, False)
                led_3 = True
                GPIO.output(LED3, True)
	    
            elif led_3 != False:
                led_3 = False
                GPIO.output(LED3, False)

    # Per evitar tenir algun dispositiu lluminos ences al sortir del programa, els parem tots.
    GPIO.output(LED1, False)
    GPIO.output(LED2, False)
    GPIO.output(LED3, False)
    exit()
