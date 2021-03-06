#!/usr/bin/env python
# -*- coding: utf8 -*-

import time
import sqlite3
import MFRC522
import datetime
import os
import signal
import RPi.GPIO as GPIO

def read():
    
    ''' 
    Lit les code en continue 
    '''

    global status
    global autorisation
    global sortie

    continue_reading = True

    # Capture SIGINT for cleanup when the script is aborted
    def end_read(signal,frame):
        global continue_reading
        print 'FIN DE LECTURE'
        continue_reading = False
        GPIO.cleanup()

    # Hook the SIGINT
    signal.signal(signal.SIGINT, end_read)

    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    #print "CTRL+C POUR STOPPER LA LECTURE"

    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while continue_reading:

        # Scan for cards
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # This is the default key for authentication
            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

            # Check if authenticated
            if status == MIFAREReader.MI_OK:
                codeLu = MIFAREReader.MFRC522_Read(8)
                MIFAREReader.MFRC522_StopCrypto1()

                #On converti le code en string
                codeCarte = lstToString(codeLu)

                #On cherche le code dans la base de donnnee
                rechercheIdentifiant(codeCarte)
                time.sleep(2)
                os.system('clear')

            else:
                autorisation = False
                print 'ERREUR D\'AUTHENTIFICATION'
                print 'ACCES REFUSE'
                redBlink(8)
                time.sleep(2)
                os.system('clear')
                
def lstToString(codeLecteur):

    ''' 
    Convertis une liste en string 
    '''

    global codeCarte
    codeCarte = ''
    for i in codeLecteur:
        codeCarte += str(i)

    return codeCarte

def rechercheIdentifiant(codeCarte):

    ''' 
    Recherche un code dans une base de donnees sqlite
    et donne acces ou non en fonction du code 
    '''

    global cursor
    global sortie
    global autorisation
    
    #On se connecte à la base
    conn = sqlite3.connect('datab.db')
    cursor = conn.cursor()

    #On prend toute la base de donnee et la stock dans une liste
    cursor.execute("""SELECT CODE, STATUT, NOM, PRENOM, REGIME FROM base""")
    liste = cursor.fetchall()

    #Le code est dans la base
    try:

          carteValide = True

          #On cherche le code
          i = 0
          while liste[i][0] != codeCarte:
                 i += 1

          statut = str(liste[i][1])
          nom = str(liste[i][2])
          prenom = str(liste[i][3])
          regime = '('+str(liste[i][4])+')'

          #C'est un eleve
          if str(liste[i][1]) == 'ELEVE':
                 sortie = statut +' : '+ nom +' '+ prenom +' '+ regime

          #C'est un professeur ou un agent
          else:
                 sortie = statut +' : '+ nom +' '+ prenom

    #Le code n'est pas dans la base
    except IndexError:
          carteValide = False
          sortie = 'CARTE NON VALIDE'

    #La carte est valide
    if carteValide == True:

          #L'heure
          date = time.localtime()

          #La date
          ajourdHui = datetime.datetime.today()
          
          #Le jour de la semaine
          jour = ajourdHui.weekday()
          
          #On l'heure en minute
          minute = date[4]+60*date[3] 

          #C'est un professeur 
          if statut == 'PROFESSEUR':


                 #On n'est pas le weekend
                 if jour != 5 and jour != 6:
                     autorisation = True
                                         
                 #On est le weekend
                 else:
                     autorisation = False
    
          #C'est un agent
          elif statut == 'AGENT':
                 autorisation = True

          #C'est un eleve

          else:

                 #Il est entre 7H30 et 18H30
                 if 450 <= minute <= 1110:

                     #On n'est pas le weekend
                     if jour != 5 and jour != 6:
                         autorisation = True
                         
                     #On est le weekend
                     else:
                         autorisation = False
        
                 #Hors plage horaire
                 else:
                        autorisation = False

    #La carte n'est pas vadlide
    else:

          autorisation = False

    if autorisation:
        sortie += '\n'+'ACCES AUTORISE'+'\n'
        print sortie
        greenBlink(3)
    else:
        sortie += '\n'+'ACCES REFUSE'+'\n'
        print sortie
        redBlink(8)

def greenBlink(greenPin):
    
    '''
    Fais clignoter la LED verte
    '''
    
    GPIO.setup(greenPin,GPIO.OUT)
    
    for i in range(2):
        GPIO.output(greenPin,GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(greenPin,GPIO.LOW)
        time.sleep(.1)
        
    GPIO.output(greenPin,GPIO.HIGH)
    time.sleep(.5)
    GPIO.output(greenPin,GPIO.LOW)

def redBlink(redPin):
    
    '''
    Fais clignoter la LED rouge
    '''
    
    GPIO.setup(redPin,GPIO.OUT)
    
    for i in range(4):
        GPIO.output(redPin,GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(redPin,GPIO.LOW)
        time.sleep(.1)
        
    GPIO.output(redPin,GPIO.HIGH)
    time.sleep(.5)
    GPIO.output(redPin,GPIO.LOW)


    
