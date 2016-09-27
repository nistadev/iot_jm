#!/urs/bin/python3
import os
import sys

#Variables globals
INET = False 
button4 = False

#Comprovem els arguments que rebem per a determinar 
#si tenim una connexio a internet.
if sys.argv[1] == "1":
    INET = True
else:
    INET = False

#Comencem el programa mentres no s'apreti el quart boto
while not button4: #.actiu():
    if INET:
	print("El dispositiu esta connectat a internet. Provant de enviar \
	    les dades.")
    else:
	print("El dispositiu no disposa de una connexio a internet. \
	    Creant un fitxer per a guardar les dades...")
