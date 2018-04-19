import sqlite3

conn = sqlite3.connect('datab.db')
cursor = conn.cursor()

def rechercheIdentifiant(idCarte):
       global cursor
       cursor.execute("SELECT CODE, STATUT, NOM, PRENOM, REGIME FROM base")
       liste = cursor.fetchall()
       try:
              validite = True
              i = 0
              while liste[i][0] != idCarte:
                     i += 1

              if str(liste[i][1]) == 'ELEVE':
                     sortie = str(liste[i][1])+' : '+str(liste[i][2])+' '+str(liste[i][3])+' '+'('+str(liste[i][4])+')'
              else:
                     sortie = str(liste[i][1])+' : '+str(liste[i][2])+' '+str(liste[i][3])
                                   
       except IndexError:
              validite = False
              sortie = 'CARTE NON VALIDE'
              
       print(sortie)
       return sortie

code = 6659530427386586
rechercheIdentifiant(str(code))
