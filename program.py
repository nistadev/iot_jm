#!/urs/bin/python3

""" 
Aquest programa envia les dades al nuvol, a un full de calcul de Google en cas de tenir INET,
sino crea un fitxer on hi desa les dades capturades en un mateix dia. També envia les dades guardades
si l'usuari vol fer-ho.

Tot el programari que forma part de la llibreria del sensor de humitat i llum, estan subjectes a la següent llicència, 
tal i com l'autor inicial l'ha distribuït:

The MIT License (MIT)

Copyright (c) 2014 Adafruit Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
from needs import *
from valorlux import *

#Execucions previes
inicialitza()

#Variables globals
INET = False 
DHT_TYPE = Adafruit_DHT.DHT22 # Sensor de Himitat i Temperatura
DHT_PIN = 13 # Pin del sensor
GAUTH = "autenticacio.json" # Fitxer que guarda les credencials per a poder guardar les dades.
GSPREAD = "Dades de Llum, Temperatura i Humitat" # Nom de la nostra fulla de calcul.
fullcalcul = None 
tsl = TSL2561() # Sensor de lluminositat
in_progress = False
diaAvui = '{:%Y/%m/%d}'.format(datetime.datetime.today()) # Data d'avui en format AAAA/MM/DD
nomFitxer = "{:%Y-%m-%d}.json".format(datetime.datetime.today()) # Nom del fitxer basat en la data d'avui.
dadesNoves = {} # Diccionari per a guardar dades noves en fitxer.

#Funcions
def set_inet():
    """ Comprova els arguments que rebem per a determinar si tenim una connexio a internet o no """
    global INET
    if sys.argv[1] == "1":
        INET = True
    else:
        INET = False


def google_login(fitxer_clau_oauth):
    """Es connecta a Google Docs i retorna el primer full de calcul."""
    try:
        scope = ['https://spreadsheets.google.com/feeds']
        credencialsAcces = ServiceAccountCredentials.from_json_keyfile_name(fitxer_clau_oauth, scope)
        connexGoogle = gspread.authorize(credencialsAcces)
        fullcalcul = connexGoogle.open(GSPREAD).sheet1
        return fullcalcul
    except Exception as ex:
        print("No s'ha pogut fer login a google.")
        print('Error:', ex)
        sys.exit(1)


def humitempilux():
    """ Refresca els valors de les variables de cada dada que enviem, ja sigui dels sensors o la data """
    global hum, graus, lux, hora
    humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN) # Llegeix les dades del sensor de Temperatura i Humitat
    if humidity is None or temp is None: # En cas de fallar algun dels 2, torna a comprovar.
        humitempilux()
    else:
        hum = int("{0:0.1f}".format(humidity)) # Guardem les dades en la variable corresponent
        graus = int("{0:0.1f}".format(temp))

    if tsl.foundSensor(): # En cas de que trobi un sensor de llum, captura les dades.
        tsl.setGain(tsl.GAIN_16X) # Potencia (podriem dir que la sensibilitat del sensor...)
        tsl.setTiming(tsl.INTEGRATIONTIME_13MS) # Temps entre lectura
        visible = tsl.getLuminosity(tsl.VISIBLE) # Lux que volem que ens mostri
        lux = int("{0}".format(visible)) # Guardem la dada de la lectura en la variable
    else:
        lux = "Error" #Si no troba sensor, envia el valor "Error"

    hora = "{:%Y/%m/%d %H:%M:%S}".format(datetime.datetime.today()) # Guarda la hora en format AAAA/MM/DD hh:mm:ss


def enviar():
    """ Mostra per pantalla les dades per a enviar i les envia, tambe engega els leds segons el estat de la tasca """
    global fullcalcul, graus, lux, hora, hum

    if fullcalcul is None: # En cas de que no hi hagi un full de calcul guardat, prova de tornar a fer login
        fullcalcul = google_login(GAUTH)

    encen(LED2)
    print("\nEnviant dades...")
    humitempilux()
    print('Temperature: {0}C'.format(graus))
    print('Humidity:    {0}%'.format(hum))
    print('Lux:         {0}'.format(lux))

    try: # Provem de adjuntar la informacio a la ultima fila
        fullcalcul.append_row((hora, lux, graus, hum)) 
    except:
        print('Error al enviar les dades.')
        apaga(LED2)
        encen(LED3)
        ts(1)
        apaga(LED3)
        fullcalcul = None
        ts(SEGONS)
        break
    print('Dades enviades correctament.')
    apaga(LED2)
    encen(LED1)
    #Espera els segons establerts abans de continuar
    ts(SEGONS)


def enviarFitxer(data, l, g, h):
    """ Agafa com a parametres les dades del fitxer guardat i prova de enviar-les al nuvol """
    global fullcalcul

    if fullcalcul is None:
        fullcalcul = google_login(GAUTH)

    encen(LED2)
    print("\nEnviant les dades del fitxer...")
    try:
        fullcalcul.append_row((data, l, g, h))
    except:
        print('Error al enviar les dades.')
        apaga(LED2)
        encen(LED3)
        ts(1)
        apaga(LED3)
        fullcalcul = None
        ts(SEGONS)
    print('Dades enviades correctament.')
    apaga(LED2)
    encen(LED1)
    #Espera els segons establerts abans de continuar
    ts(SEGONS)


def guardar():
    """ Aqui es on hi ha la feina grossa... Son conceptes simples pero que m'han donat molts problemes. La funcio basicament
        el que fa es crear provar de crear un fitxer tenint com a nom la data d'avui (per a no guardar en molts fitxers diferents
        cada lectura que fem) i en cas de fallar -perque el fitxer esta creat ja- guarda noves dades al fitxer. Aquest proces
        de guardar les noves dades ha sigut complicat, i ara veureu perque... :) """
    try:
        nouFitxerDades = open("dades_sensors/{0}".format(nomFitxer), 'x') # Provem de crear el fitxer
        print("\nCreant fitxer per desar les dades d'avui...")

        encen(LED2)
        print("Captant les dades...")
        humitempilux() # Capturem noves dades
        
        print("Desant les dades...")
        dadesNoves['lectura0'] = {}
        dadesNoves['lectura0']['humitat'] = hum
        dadesNoves['lectura0']['temperatura'] = graus
        dadesNoves['lectura0']['llum'] = lux
        dadesNoves['lectura0']['dataIhora'] = hora
        json.dump(dadesNoves, nouFitxerDades) # Guardem les noves dades en el fitxer de format '.json'
        nouFitxerDades.close() # Tanquem el fitxer!! Molt important per a que es guardin les dades.
        print("Dades desades correctament!\n")

        apaga(LED2)
        encen(LED1)
        ts(SEGONS - 1.5)

    except:
        print("\nAfegint noves dades al fitxer d'avui...")
        fitxerDades = open('dades_sensors/{0}'.format(nomFitxer), 'r') # Obrim el fitxer ja creat i amb dades en mode lectura
        accesFitxer = json.load(fitxerDades) # Guardem les dades en una variable
        fitxerDades.close() # Tanquem el fitxer

        encen(LED2)
        print("Captant les dades...")
        humitempilux() # Capturem noves dades per a afegir
        
        print("Desant les dades...")
        numLectura = len(accesFitxer) # Comprovem quants elements hi ha a dins del fitxer per a saber el nom de la lectura
        accesFitxer['lectura{}'.format(numLectura)] = {}
        accesFitxer['lectura{}'.format(numLectura)]['humitat'] = hum
        accesFitxer['lectura{}'.format(numLectura)]['temperatura'] = graus
        accesFitxer['lectura{}'.format(numLectura)]['llum'] = lux
        accesFitxer['lectura{}'.format(numLectura)]['dataIhora'] = hora
        try:
            fitxerTemporal = open('dades_sensors/temp.json', 'x') # Provem de crear un fitxer temporal a on guardem les noves dades
            json.dump(accesFitxer, fitxerTemporal) # Guardem les dades al fitxer temporal
            fitxerTemporal.close()
        except:
            fitxerTemporal = open('dades_sensors/temp.json', 'r') # En cas de que no ens el deixi crear, l'obrim i copiem les dades d'aquest
        fitxerDades = open('dades_sensors/{0}'.format(nomFitxer), 'w')
        fitxerTemporal = open('dades_sensors/temp.json', 'r')
        accesFitxerTemporal = json.load(fitxerTemporal)
        fitxerTemporal.close()
        json.dump(accesFitxerTemporal, fitxerDades) # Finalment, escrivim les noves dades al fitxer que ja teniem.
        fitxerDades.close()
        print("Dades desades correctament!\n")

        os.remove("dades_sensors/temp.json") # Eliminem el fitxer temporal
        apaga(LED2)
        encen(LED1)
        ts(SEGONS - 1.5)


def llegir(enviar):
    """ Processa les dades dels fitxers, les mostra per pantalla si no tenim INET i les envia si en tenim """
    if enviar == 0: # Determinem si tenim interet o no segons el parametre que rebem.
        fitxerDadesGuardades = open('dades_sensors/{0}'.format(nomFitxer), 'r')
        procDades = json.load(fitxerDadesGuardades) # Carreguem el fitxer per a processar les dades.

        print('\nDades del dia {0}:'.format(diaAvui)) # Comencem el proces de mostrar les dades.
        for e in procDades:
            print('\n' + e + ':')
            for i in procDades[e]:
                print(i + ' == ' + str(procDades[e][i]))
            ts(.5)
    else:
        #En cas de que tinguem internet prova a enviar les dades d'avui en cas de que en quedin per enviar.
        encen(LED2)
        try:
            global dthr, lx, gr, hm            
            fitxerDadesGuardades = open('dades_sensors/{0}'.format(nomFitxer), 'r')
            procDades = json.load(fitxerDadesGuardades)
            fitxerDadesGuardades.close()
            for e in procDades: # Per cada lectura, obte el valor de cada sensor i la guarda en una variable
                for i in procDades[e]:
                    if i == 'dataIhora':
                        dthr = procDades[e][i]
                    elif i == 'humitat':
                        hm = procDades[e][i]
                    elif i == 'llum':
                        lx = procDades[e][i]
                    elif i == 'temperatura':
                        gr = procDades[e][i]

                enviarFitxer(dthr, lx, gr, hm) # Enviem les dades com a parametres
            fitxerDadesGuardades.close()
            os.remove("dades_sensors/{0}".format(nomFitxer)) # Un cop hem enviat les dades, eliminem el fitxer per no ocupar espai
                                                             # ja que ja tenim les dades guardades al nuvol.
            encen(LED1)

        except: # En cas de que no trobi cap fitxer de la data d'avui per enviar, ens avisa
            print('No hi han dades guardades per enviar...\n')
            apaga(LED2)
            ts(.5)
            encen(LED3)
            ts(1)
            apaga(LED3)
        
       
set_inet() # Comprovem la connexio a INET
program_running(1) # Avisem de que ens trobem en el primer programa
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
            """ Quan l'usuari premi el primer boto, comencara a capturar dades i enviarles o guardarles en funcio de la connexio """
            in_progress = True
            while True:
                ts(seconds)
                button_4 = GPIO.input(BUTTON4)
                if (button_4 != actiu):
                    if INET:
                        # En cas de tenir INET, enviar les dades mentre l'usuari no apreti el quart boto
                        enviar()
                        apaga(LED1)
                    else:
                        # En cas de fallar INET, guardar les dades mentre l'usuari no apreti el quart boto
                        guardar()
                        apaga(LED1)

                else:
                    print("Proces cancelat. Tornant al programa inicial.")
                    break

            in_progress = False

        if button_2 == actiu and not in_progress:
            """ Si l'usuari apreta el segon boto, en cas de tenir internet s'enviaran les dades pendents al nuvol, sino
                es mostraran les dades que tenim guardades per pantalla """
            in_progress = True
            while True:
                ts(seconds)
                button_4 = GPIO.input(BUTTON4)
                if (button_4 != actiu):
                    if INET:
                        llegir(1)
                        apaga(LED1)
                    else:
                        llegir(0)
                        apaga(LED1)
                else:
                    print("Proces cancelat. Tornant al programa inicial.")
                    break

            in_progress = False

        if button_3 == actiu and not in_progress:
            """ En cas de premer el tercer boto, se li mostrara una senyal lluminosa per a que sapiga a quin programa es troba """
            in_progress = True
            val = True
            num = 0
            program_running(1)
            in_progress = False


    exit()
