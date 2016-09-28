#!/usr/bin/python

#Llibreries
import os
import ifaddr
import time
import RPi.GPIO as GPIO
from gpiozero import LED, Button

#Execucions previes
GPIO.setmode(GPIO.BCM)

#Variables globals
BUTTON1 = 6
BUTTON2 = 5
BUTTON3 = 25
BUTTON4 = 24
APON = 0
ETHON = 0
adapters = ifaddr.get_adapters()
INTFC = "eth0"
apretat = 0
seconds = 0.5

#Inicialitacio components GPIO
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Funcio principal per a comprovar la connexio, basada en si tenim una IP assignada.
def adapter_check():
    global ETHON
    """ Comprova si l'adaptador te una IP """
    for adapter in adapters:
    	if adapter.name == INTFC:
            print("L'adaptador esta online i te assignada la IP {}".format(adapter.ips[0].ip))
            ETHON = 1
	else:
	    pass

adapter_check()

def ts(temps):
    """ Retorna una pausa del temps especificat en segons """
    return time.sleep(temps)

def enter_program(number):
    """ Entra en el programa corresponent al boto donant el numero i si no ens trobem dins de un altre programa """
    if (number == 1):
	print(ETHON)
	os.system("python program.py {0}".format(ETHON))	
	ts(seconds)
	pre_boto()

    elif (number == 2):
	os.system("python tester.py")
	ts(seconds)
	pre_boto()

    elif (number == 3):
	pass

    elif number == 4:
	exit()

def pre_boto():
    print("Premi un boto per a executar el programa que vulgui")
    while True:
        """ Loop que comprova si un usuari ha apretat algun boto i executa la funcio que obrira el programa corresponent """ 
        button_1 = GPIO.input(6)
	button_2 = GPIO.input(5)
	button_3 = GPIO.input(25)
	button_4 = GPIO.input(24)
	
        #Comprovem quin es el boto que ha apretat l'usuari i executem la funcio que obria el programa.
	#print(button_1, button_2, button_3, button_4)	
        if button_1 == apretat:
	    ts(seconds)
	    enter_program(1)

        if button_2 == apretat:
	    ts(seconds)
    	    enter_program(2)

        if button_3 == apretat:
	    #ts(seconds)
	    #enter_program(3)
	    pass

        if button_4 == apretat:
	    ts(seconds)
	    enter_program(4)
	

pre_boto()
