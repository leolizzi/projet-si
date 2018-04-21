#!/usr/bin/env python
# -*- coding: utf8 -*-

import time
import sqlite3

def lstToString(codeLecteur):
    
    ''' Convertis un string en une liste '''
    
    global codeCarte
    codeCarte = ''
    for i in codeLecteur:
        codeCarte += str(i)
        
    return codeCarte

def rechercheIdentifiant(codeCarte):

    ''' Recherche un code dans une base de sonnée sqlite '''

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
          sortie = '\n'+'CARTE NON VALIDE'+'\n'
          
    #La carte est valide
    if carteValide == True:

          #C'est un professeur
          if statut == 'PROFESSEUR':
                 autorisation = True
                 sortie += '\n'+'ACCES AUTORISE'+'\n'

          #C'est un agent
          elif statut == 'AGENT':
                 autorisation = True
                 sortie += '\n'+'ACCES AUTORISE'+'\n'

          #C'est un eleve
          else:
                 date = time.localtime()
                 
                 #On passe tout en minute
                 minute = date[4]+60*date[3]

                 #L'heure permet à un eleve de rentrer (450min:7H30 et 1110:18H30)
                 if 450 <= minute <= 1110:
                        autorisation = True
                        sortie += '\n'+'ACCES AUTORISE'+'\n'

                 #L'heure ne permet pas à un eleve de rentrer
                 else:
                        autorisation = False
                        sortie += '\n'+'ACCES REFUSE'+'\n'

    #La carte n'est pas valide
    else:
          sortie += '\n'+'ACCES REFUSE'+'\n'
                 
    return sortie

