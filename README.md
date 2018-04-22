# projet-si

Matériel:

- Capteur RFiD RC522 (avec ses tags à 13,56MHz)
- Raspberry Pi 3
- Language Python2 (du fait de la librairie)
- Sqlite3 et une base de donnée (.db)

Ce projet à pour but d'autoriser ou non le passage d'élèves, professeurs et agents de maintenance en fonction de leurs statut.

- Les élèves sont autorisés à passer entre 7H30 et 18H30 hors weekends.
- Les professeurs sont autorisés à passer tous le temps hors weekends.
- Les agents de maintenance sont tous le temps autorisés, weekends compris.

Chaque personne est consignée dans une base de donnée (datab.db) suivant l'agencement suivant:

- Première ligne : CODE
- Deuxième ligne : STATUT
- Troisième ligne : NOM
- Quatrième ligne : PRENOM
- Cinquième ligne : REGIME

(Chaque ligne représente donc une personne)

Quand une personne passe son tag RFiD devant le lecteur, on lit le code et le cherche dans la base de donnée à l'aide du programme Read.py. 
Si il n'y est pas on refuse le passage. Si il y est, alors on lit les informations relative à cette personne et les affiche (NOM PRENOM et éventuellement REGIME pour les élèves).
En fonction de son statut on le laisse passer selon les conditions définies précédemment.

Le programme attend 2s après chaque passage de tag, efface les informations à l'écran avant de tenter de lire un nouveau tag.

Généralement, neufs les tags RFiD contiennnent les valeurs 0000[...]0, alors on assigne une nouvelle valeur au tag à l'aide du programme Write.py et on rajoute une personne avec ce code à la base de donnée avec le programme ajoutBase ou ajoutBase_glade.py (Affichage graphique).





