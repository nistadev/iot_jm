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
        GPIO.setup(self._pin, GPIO.IN, pud_up_down=DOWN)

    def status(self):
        return self._status

    def set_status(self, value):
        self._status = value


#Variables globals
APON = 0
ETHON = 0
adapters = ifaddr.get_adapters()
INTFC = "eth0"
tries = 0
program_1 = False
program_2 = False

#Funcio principal per a comprovar la connexio, basada en si tenim una IP assignada.
def adapter_check():
    """ Check if adapter has an IP """
    for adapter in adapters:
        if adapter.name == INTFC:
            print("L'adaptador esta online i te assignada la IP {}".format(adapter.ips[0].ip))
            ETHON = True
        else:
            pass

    tries += 1
