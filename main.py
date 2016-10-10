#!/usr/bin/python3

#Llibreries
import os
import netifaces
import time
import RPi.GPIO as GPIO
from needs import *

#Execucions previes
inicialitza()

#Variables globals
APON = 0
ETHON = 0
adapter = netifaces.interfaces()
INTFC = "eth0"

#Funcions
def adapter_check(): #Funcio principal per a comprovar la connexio, basada en si tenim una IP assignada.
    """ Comprova en la llista de adaptadors disponibles si l'adaptador que ens interesa te una IP """
    global ETHON
    for a in adapter:
        if a == INTFC:
            if netifaces.ifaddresses(INTFC)[2][0]["addr"]:
                print("L'adaptador d'internet esta online i te assignada la IP {0}".format(netifaces.ifaddresses(INTFC)[2][0]["addr"]))
                ETHON = 1
            else:
                print("L'adaptador d'internet no esta online. Crearem un fitxer per a guardar les dades.")
        else:
            pass

def pre_stop():
    val = True
    for i in range(2):
        """ Encen i apaga els leds segons la variable val """
        GPIO.output(LED1, val)
        GPIO.output(LED2, val)
        GPIO.output(LED3, val)
        ts(0.1)
        if val:
            val = False
        elif not val:
            val = True

def enter_program(number):
    """ Entra en el programa corresponent al boto donant el numero i si no ens trobem dins de un altre programa """
    if (number == 1):
        print("Entrant en el programa del processament de les dades...\n")
        os.system("python3 program.py {0}".format(ETHON))	
        ts(seconds)
        pre_boto()

    elif (number == 2):
        print("Entrant en el programa de fer tests al maquinari...\n")
        os.system("python3 tester.py")
        ts(seconds)
        pre_boto()

    elif (number == 3):
        ts(seconds)
        pre_boto()

    elif number == 4:
        pre_stop()
        GPIO.cleanup()
        exit() #os.system("sudo poweroff")

def pre_boto():
    """ Funcio que ens posa en un estat d'espera per a que l'usuari esculli el que vol fer. """
    program_running(0)
    adapter_check() #Fem la comprovacio de l'adaptador de xarxa cada cop, per a estar informats sempre.
    print("\nPremi un boto per a executar el programa que vulgui")
    while True:
        """ Loop que comprova si un usuari ha apretat algun boto i executa la funcio que obrira el programa corresponent """ 
        button_1 = GPIO.input(BUTTON1)
        button_2 = GPIO.input(BUTTON2)
        button_3 = GPIO.input(BUTTON3)
        button_4 = GPIO.input(BUTTON4)
	
        #Comprovem quin es el boto que ha apretat l'usuari i executem la funcio que obria el programa.	
        if button_1 == actiu:
            ts(seconds)
            enter_program(1)

        if button_2 == actiu:
            ts(seconds)
            enter_program(2)

        if button_3 == actiu:
            ts(seconds)
            enter_program(3)

        if button_4 == actiu:
            ts(3.5)
            button_4 = GPIO.input(BUTTON4)
            if button_4 == actiu:
                enter_program(4)
	    else:
		pass

#--------------------
# Inici del programa
#--------------------
pre_boto()
