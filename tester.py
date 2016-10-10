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
from needs import *

#Inicialitzacions previes
inicialitza()

#Variables Globals
DHT_TYPE = DHT.DHT22
DHT_PIN = 13 
apretat = 0
seconds = 0.5
led_1 = False
led_2 = False
led_3 = False

#Variables objecte
button_1 = GPIO.input(BUTTON1)
button_2 = GPIO.input(BUTTON2)
button_3 = GPIO.input(BUTTON3)
button_4 = GPIO.input(BUTTON4)
tsl = TSL2561()

# Funcions
def gethyt():
    """ Guarda les dades llegides per el sensor de temperatura i humitat en les respectives variables globals """
    global hum, temp
    hum, temp = DHT.read(DHT_TYPE, DHT_PIN)


""" Inici del programa """

program_running(2) # Executem la funcio d'inici abans d'entrar al loop

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
        if (button_1 == actiu) and (not testing):
            testing = True
            print("Calculant els lux...")
            GPIO.output(LED3, True)
            ts(seconds)
            if tsl.foundSensor():
                tsl.setGain(tsl.GAIN_16X); #Pot ser 0X o 16X
                tsl.setTiming(tsl.INTEGRATIONTIME_13MS)
                visible = tsl.getLuminosity(tsl.VISIBLE)
                print("Lux: {0}".format(visible))
                GPIO.output(LED3, False) # Encenem i apaguem els LEDs de vermell a verd per indicar
                GPIO.output(LED2, True)  # a l'usuari que hem captat les dades correctament.
                ts(seconds)
                GPIO.output(LED2, False)
                GPIO.output(LED1, True)
                ts(seconds)
                GPIO.output(LED1, False)
            else:
                print("Error. Hi ha sensor?")
            testing = False
	
        if (button_2 == actiu) and (not testing):
            testing = True
            ts(seconds)
            print("Calculant la temperatura i la humitat...")
            GPIO.output(LED3, True)
            gethyt()
            if (hum != None) and (temp != None):
                print("Temperatura: {0:0.1f}".format(temp))
                print("Humitat: {0:0.1f}\n".format(hum))
                GPIO.output(LED3, False)
                GPIO.output(LED2, True)
                ts(seconds)
                GPIO.output(LED2, False)
                GPIO.output(LED1, True)
                ts(seconds)
                GPIO.output(LED1, False)
            else:
                print("Error al captar les dades amb el sensor, torneu-ho a provar mes tard.\n")
            testing = False
	
        if (button_3 == actiu):
            ts(seconds)
            # Comprovem en quina fase de l'accio es troba per determinar si encenem/apaguem un led
            if (led_1 != True) and (led_2 != True) and (led_3 != True):
                led_1 = True
                print("Encenent el LED verd...") # Mostrem per pantalla l'estat en el que ens trobem per a 
                GPIO.output(LED1, True)          # dornar mes informacio a l'usuari.

            elif (led_1 != False):
                led_1 = False
                GPIO.output(LED1, False)
                led_2 = True
                print("Encenent el LED groc...")
                GPIO.output(LED2, True)

            elif (led_2 != False):
                led_2 = False
                GPIO.output(LED2, False)
                led_3 = True
                print("Encenent el LED vermell...")
                GPIO.output(LED3, True)

            elif (led_3 != False):
                led_3 = False
                print("LEDs apagats.\n")
                GPIO.output(LED3, False)

    # Per evitar tenir algun dispositiu lluminos ences al sortir del programa, els parem tots.
    GPIO.output(LED1, False)
    GPIO.output(LED2, False)
    GPIO.output(LED3, False)
    exit()
