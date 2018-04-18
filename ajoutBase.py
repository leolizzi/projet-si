# -*- coding: utf-8 -*-

import sqlite3

try:
    conn = sqlite3.connect('datab.db')
    cursor = conn.cursor()

    code = 'CODE'
    statut = 'ELEVE'
    nom = 'NOM1'
    prenom = 'PRENOM1'
    regime = 'INTERNE'

    cursor.execute("""INSERT INTO base VALUES(?,?,?,?,?)""",(code,statut,nom,prenom,regime))

    conn.commit()
    cursor.close


except sqlite3.OperationalError:
    print('La base de donnée est probablement en cours d\'utilisation. Fermez l\'instance et réessayez !')


