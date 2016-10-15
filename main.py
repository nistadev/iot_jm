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
INET = 0
INTFC = "eth0" # Interficie que ens determina la connexio
adapter = netifaces.interfaces() # Retorna una llista amb les connexions i IP's, si la llista te
                                 # mes de 2 elements vol dir que tenim una connexio a internet.

#Funcions
def adapter_check():
    """ Funcio principal per a comprovar la connexio, basada en si tenim una IP assignada.
        Comprova en la llista de adaptadors disponibles si l'adaptador que ens interesa te una IP i modifica el valor de "INET",
        que es la variable que fem servir per a saber si tenim connexio o no.
    """
    global INET
    for a in adapter:
        if a == INTFC:
            if len(netifaces.ifaddresses(INTFC)) > 2: # Comprovem que la llargada es mes gran de 2 per a saber si tenim INET
                print("L'adaptador d'internet esta online i te assignada la IP {0}".format(netifaces.ifaddresses(INTFC)[2][0]["addr"]))
                INET = 1
            else:
                print("L'adaptador d'internet no esta online. Crearem un fitxer per a guardar les dades.")
        else:
            pass

def pre_stop():
    val = True
    for i in range(2):
        """ Encen i apaga els leds segons la variable val per a mostrar que pararem el dispositiu """
        if val:
            encen(LED1)
            encen(LED2)
            encen(LED3)
            ts(.1)
            val = False
        elif not val:
            apaga(LED1)
            apaga(LED2)
            apaga(LED3)
            val = True

def enter_program(number):
    """ Entra en el programa corresponent al boto segons el parametre que rebem """
    if (number == 1):
        print("Entrant en el programa del processament de les dades...\n")
        os.system("python3 program.py {0}".format(INET))	
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

    elif (number == 4):
        pre_stop()
        GPIO.cleanup()
        os.system("sudo poweroff")

def pre_boto():
    """ Funcio que ens posa en un estat d'espera per a que l'usuari esculli el que vol fer """
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
            """ Avisem a l'usuari que volem parar el dispositiu, i esperem 3-4 segons per a evitar que es pari a la minima.
                Si l'usuari mante el boto apretat, la variable "button_4" tinra el valor de "actiu" i per tant entrara en la funcio.
                Aixo evita que l'usuari pari l'aparell involuntariament """

            print('Continui prement el boto per a parar el dispositiu...')
            ts(1)
            print('Parant en 3...')
            ts(1)
            print(' 2...')
            ts(1)
            print(' 1...')
            ts(1)
            button_4 = GPIO.input(BUTTON4)
            if button_4 == actiu:
                print('Parant el dispositiu.')
                enter_program(4)
	

#--------------------
# Inici del programa
#--------------------
pre_boto()
