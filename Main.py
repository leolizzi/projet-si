#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import time
import os
import signal
from fonctions import *

#Lis les tags en continu
read()

#Verifie l'authentification
if status == MIFAREReader.MI_OK:
    codeLu = MIFAREReader.MFRC522_Read(8)
    MIFAREReader.MFRC522_StopCrypto1()

    #On converti le code en string
    codeCarte = lstToString(codeLu)

    #On cherche le code dans la base de donnnee
    print rechercheIdentifiant(codeCarte)
    time.sleep(2)
    os.system('clear')

else:
    print 'ERREUR D\'AUTHENTIFICATION'+'\n'
    time.sleep(2)
    os.system('clear')



            
