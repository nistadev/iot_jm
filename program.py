#!/urs/bin/python3

""" Aquest programa es el que envia les dades al nuvol, a un full de calcul de Google. """

#Llibreries
import os
import sys
import time
import json
import datetime
import Adafruit_DHT
import gspread
import RPi.GPIO as GPIO
from oauth2client.service_account import ServiceAccountCredentials
from valorlux import *
from needs import *

#Execucions previes
inicialitza()

#Variables globals
INET = False 
DHT_TYPE = Adafruit_DHT.DHT22
DHT_PIN = 13
GAUTH = "autenticacio.json"
GSPREAD = "Dades de Llum, Temperatura i Humitat"
worksheet = None
tsl = TSL2561()
in_progress = False

#Funcions
def set_inet():
    """ Comprova els arguments que rebem per a determinar si tenim una connexio a internet o no"""
    global INET
    if sys.argv[1] == "1":
        INET = True
    else:
        INET = False

def login_open_sheet(oauth_key_file):
    """Connect to Google Docs spreadsheet and return the first worksheet."""
    try:
        scope =  ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
        gc = gspread.authorize(credentials)
        worksheet = gc.open(GSPREAD).sheet1
        return worksheet
    except Exception as ex:
        print('Unable to login and get spreadsheet. Check OAuth credentials, and make sure spreadsheet is shared to the client_email address in the OAuth .js')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)

def humitempilux():
    global hum, graus, lux, hora
    humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)
    if humidity is None or temp is None:
        humitempilux()
    else:
        hum = "{0:0.1f}".format(humidity)
        graus = "{0:0.1f}".format(temp)

    if tsl.foundSensor():
        tsl.setGain(tsl.GAIN_16X)
        tsl.setTiming(tsl.INTEGRATIONTIME_13MS)
        visible = tsl.getLuminosity(tsl.VISIBLE)
        lux = int("{0}".format(visible))
    else:
        lux = "Error"   

    avui = datetime.datetime.today()
    hora = "{:%Y/%m/%d %H:%M:%S}".format(avui)

def enviar():
    global worksheet, graus, lux, hora, hum
    if worksheet is None:
        worksheet = login_open_sheet(GAUTH)

    GPIO.output(LED2, True)
    print("\nEnviant dades...")
    humitempilux()
    print('Temperature: {0}C'.format(graus))
    print('Humidity:    {0}%'.format(hum))
    print('Lux:         {0}'.format(lux))
    graus = float(graus)
    hum = float(hum)
    # Append the data in the spreadsheet, including a timestamp
    try:
        worksheet.append_row((hora, lux, graus, hum))
    except:
        print('Error al enviar les dades.')
        GPIO.output(LED2, False)
        GPIO.output(LED3, True)
        ts(1)
        GPIO.output(LED3, False)
        worksheet = None
        ts(SEGONS)
    print('Dades enviades.')
    GPIO.output(LED2, False)
    GPIO.output(LED1, True)
    #Espera els segons establerts abans de continuar
    ts(SEGONS)

set_inet()
program_running(1)
while True:
    """ Comencem el programa mentres no s'apreti el quart boto """
    button_4 = GPIO.input(BUTTON4)
    print("Premi un boto per a comencar els processament de les dades.")
    while (button_4 != actiu):
        button_1 = GPIO.input(BUTTON1) # Actualitzem els valors dels botons a cada volta.
        button_2 = GPIO.input(BUTTON2)
        button_3 = GPIO.input(BUTTON3)
        button_4 = GPIO.input(BUTTON4)

        if button_1 == actiu and not in_progress:
            in_progress = True
            while True: #for i in range(10):
                ts(seconds)
                button_4 = GPIO.input(BUTTON4)
                if (button_4 != actiu):
                    if INET:
                        enviar()
                        GPIO.output(LED1, False)
                    else:
                        try:
                            pass
                        except:
                            print("El dispositiu no disposa de una connexio a internet. Creant un fitxer per a guardar les dades...")
                            ts(1)
                else:
                    print("Proces cancelat. Tornant al programa inicial.")
                    break

            in_progress = False

        if button_2 == actiu and not in_progress:
            in_progress = True
            if INET:
                enviar()
                GPIO.output(LED1, False)
            else:
                try:
                    pass
                except:
                    print("El dispositiu no disposa de una connexio a internet. Creant un fitxer per a guardar les dades...")
                    ts(1)

            in_progress = False

        if button_3 == actiu and not in_progress:
            in_progress = True
            val = True
            num = 0
            program_running(1)
            in_progress = False


    exit()
