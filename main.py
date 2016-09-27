#!/usr/bin/python

#Llibreries
import os
import ifaddr
import time
import RPi.GPIO as GPIO

#Execucions previes
GPIO.setmode(GPIO.BCM)

#Classes
class Button:
    def __init__(self, pin, mode):
	self._pin = pin
	self._status = False
	self._mode = mode
	
    def declare(self):
	GPIO.setup(self._pin, GPIO.IN, pull_up_down=self._mode)

    def status(self):
	return self._status

    def set_status(self, value):
	""" Set the status of the button. True while it is pressed, False otherwise """
	if value == 1:
	    self._status = True
	elif value == 0:
	    self._status = False

class LED:
    def __init__(self, pin, color):
	self._pin = pin
	self._color = color
	self._status = False

    def declare(self):
	GPIO.setup(self._pin, GPIO.OUT)

    def status(self):
	return self._status

    def color(self):
	return self._color	

    def turn_on(self):
	if not self._status:
	    GPIO.output(self._pin, True)
	    self._status = True
	else:
	    pass

    def turn_off(self):
	if self._status:
	    GPIO.output(self._pin, False)
	    self._status = False
	else:
	    pass


#Variables globals
APON = 0
ETHON = 0
adapters = ifaddr.get_adapters()
INTFC = "eth0"
tries = 0
program_1 = False
program_2 = False
program_3 = False

#Variables Objecte
button_1 = Button(6, GPIO.PUD_DOWN)
button_2 = Button(5, GPIO.PUD_DOWN)
button_3 = Button(25, GPIO.PUD_DOWN)
button_4 = Button(24, GPIO.PUD_DOWN)

#Declarem els botons
button_1.declare()
button_2.declare()
button_3.declare()
button_4.declare()

#Funcio principal per a comprovar la connexio, basada en si tenim una IP assignada.
def adapter_check():
    """ Check if adapter has an IP """
    global tries
    for adapter in adapters:
    	if adapter.name == INTFC:
            print("L'adaptador esta online i te assignada la IP {}".format(adapter.ips[0].ip))
            ETHON = True
	else:
	    pass

    tries += 1

#Converteix el valor bolea en un numero binari i, en cas de que no tinguem IP assignada, ho torna a comprovar 3 vegades abans de continuar.
if ETHON:
    ETHON = 1
else:
    if tries <=2:
	adapter_check()
    else:
        ETHON = 0

#Entra en el programa corresponent al boto donant el numero i si no ens trobem dins de un altre programa
def enter_program(number):
    #global program_1, program_2, program_3
    if (number == 1) and (not program_1) and (not program_2):
	program_1 = True
	os.system("python program.py {0}".format(ETHON))
	print("Execucio despres del programa")
	time.sleep(1)
	print("yeahh")
	GPIO.cleanup()
	exit()

    elif (number == 2) and (not program_1) and (not program_2):
	program_2 = True
	os.system("python test.py")
	print("Execucio despres del programa")
	time.sleep(1)
	print("Si, es despres del programa.")
	GPIO.cleanup()
	exit()

    elif (number == 3) and (not program_1) and (not program_2):
	#program_3 = True
	pass

    elif number == 4:
	GPIO.cleanup()
	exit()


while True:
    """ Loop que comprova si un usuari ha apretat algun boto i executa la funcio que obrira el programa corresponent """

    while (not button_1.status()) and (not button_2.status()) and (not button_3.status()) and (not button_4.status()):
	""" Aquest loop es per evitar que varies execucions del programa si l'usuari continua apretant botons """
    	button_1.set_status(GPIO.input(6))
    	button_2.set_status(GPIO.input(5))
    	#button_3.set_status(GPIO.input(25))
    	button_4.set_status(GPIO.input(24))

    #Comprovem quin es el boto que ha apretat l'usuari i executem la funcio que obria el programa.
    if button_1.status():
	enter_program(1)

    elif button_2.status():
	enter_program(2)

    elif button_3.status():
	#enter_program(3)
	pass

    elif button_4.status():
	enter_program(4)
