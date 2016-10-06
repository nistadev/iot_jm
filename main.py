#!/usr/bin/python3

#Llibreries
import os
import netifaces
import time
import RPi.GPIO as GPIO

#Execucions previes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Variables globals
BUTTON1 = 6
BUTTON2 = 5
BUTTON3 = 25
BUTTON4 = 24
LED1 = 23
LED2 = 18
LED3 = 17
APON = 0
ETHON = 0
adapter = netifaces.interfaces()
INTFC = "eth0"
apretat = 0
seconds = 0.5

#Inicialitacio components GPIO
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)

#Funcions
def program_running():
    """ Funcio que mostra de manera visual que ens trobem en el programa principal """
    val = True
    for i in range(2):
        """ Encen i apaga els leds segons la variable val """
        GPIO.output(LED1, val)
        GPIO.output(LED2, val)
        GPIO.output(LED3, val)
        ts(2)
        if val:
            val = False
        elif not val:
            val = True

def adapter_check(): #Funcio principal per a comprovar la connexio, basada en si tenim una IP assignada.
    """ Comprova en la llista de adaptadors disponibles si l'adaptador que ens interesa te una IP """
    global ETHON
    for a in adapter:
        if a == INTFC:
            if netifaces.ifaddresses(INTFC)[2][0]["addr"]:
                print("L'adaptador d'internet esta online i te assignada la IP {}".format(netifaces.ifaddresses(INTFC)[2][0]["addr"]))
                ETHON = 1
            else:
                print("L'adaptador d'internet no esta online. Crearem un fitxer per a guardar les dades.")
        else:
            pass

def ts(temps):
    """ Retorna una pausa del temps especificat en segons """
    return time.sleep(temps)

def enter_program(number):
    """ Entra en el programa corresponent al boto donant el numero i si no ens trobem dins de un altre programa """
    if (number == 1):
        print(ETHON)
        os.system("python3 program.py {0}".format(ETHON))	
        ts(seconds)
        program_running()
        pre_boto()

    elif (number == 2):
        os.system("python3 tester.py")
        ts(seconds)
        program_running()
        pre_boto()

    elif (number == 3):
        program_running()
        ts(seconds)
        pre_boto()

    elif number == 4:
        GPIO.cleanup()
        exit()

def pre_boto():
    """ Funcio que ens posa en un estat d'espera per a que l'usuari esculli el que vol fer. """
    print("\nPremi un boto per a executar el programa que vulgui")
    while True:
        """ Loop que comprova si un usuari ha apretat algun boto i executa la funcio que obrira el programa corresponent """ 
        button_1 = GPIO.input(BUTTON1)
        button_2 = GPIO.input(BUTTON2)
        button_3 = GPIO.input(BUTTON3)
        button_4 = GPIO.input(BUTTON4)
	
        #Comprovem quin es el boto que ha apretat l'usuari i executem la funcio que obria el programa.
	#print(button_1, button_2, button_3, button_4)	
        if button_1 == apretat:
            ts(seconds)
            enter_program(1)

        if button_2 == apretat:
            ts(seconds)
            enter_program(2)

        if button_3 == apretat:
            ts(seconds)
            enter_program(3)
            #pass

        if button_4 == apretat:
            ts(seconds)
            enter_program(4)
	

#####################
# Inici del programa
#####################
program_running()
adapter_check()
pre_boto()
