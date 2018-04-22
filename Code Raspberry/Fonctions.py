#!/usr/bin/env python
# -*- coding: utf8 -*-

import time
import sqlite3
import datetime

def lstToString(codeLecteur):

    ''' Convertis un string en une liste '''

    global codeCarte
    codeCarte = ''
    for i in codeLecteur:
        codeCarte += str(i)

    return codeCarte

def rechercheIdentifiant(codeCarte):

    ''' Recherche un code dans une base de donnees sqlite '''
    ''' Et donne acces ou non en fonction du code '''

    global cursor
    global sortie
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

    #La carte n'est pas valide
    else:
          autorisation = False

    if autorisation == True:
        sortie += '\n'+'ACCES AUTORISE'+'\n'
    else:
        sortie += '\n'+'ACCES REFUSE'+'\n'
        
    return sortie
