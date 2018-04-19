import sqlite3
import time

#On se connecte à la base
conn = sqlite3.connect('datab.db')
cursor = conn.cursor()

def rechercheIdentifiant(codeCarte):
       global cursor
       
       #On prend toute la base de donnee et la stock dans une liste
       cursor.execute("SELECT CODE, STATUT, NOM, PRENOM, REGIME FROM base")
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

              #C'est un professeur
              if statut == 'PROFESSEUR':
                     autorisation = True
                     sortie += '\n'+'ACCES AUTORISE'

              #C'est un agent
              elif statut == 'AGENT':
                     autorisation = True
                     sortie += '\n'+'ACCES AUTORISE'

              #C'est un eleve
              else:
                     date = time.localtime()
                     heure = date[3]
                     minute = date[4]

                     #L'heure permet à un eleve de rentrer
                     if 7 <= heure <= 18 and 30 <= minute:
                            autorisation = True
                            sortie += '\n'+'ACCES AUTORISE'

                     #L'heure ne permet pas à un eleve de rentrer
                     else:
                            autorisation = False
                            sortie += '\n'+'ACCES REFUSE'

       #La carte n'est pas valide
       else:
              sortie += '\n'+'ACCES REFUSE'
                     
       print(sortie)
       return sortie

#PROFESSEUR
#codeCarte = 6659530427386586

#AGENT
#codeCarte = 5472877996915641

#ELEVE INTERNE
#codeCarte = 4367604814160025

#ELEVE EXTERNE
#codeCarte = 4141405704655090

rechercheIdentifiant(str(codeCarte))
