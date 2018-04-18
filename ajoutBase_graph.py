#!/user/bin/python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
import sqlite3
import time

class ajoutCode:
    def __init__(self):
        interface = Gtk.Builder()
        interface.add_from_file('ajoutBase.glade')

        global cursor
        global conn

        conn = sqlite3.connect('datab.db')
        cursor = conn.cursor()

        window = interface.get_object('window1')
        window.show_all()        
        
        self.Label = interface.get_object('label6')

        self.Entry1 = interface.get_object('entry1')
        self.Entry2 = interface.get_object('entry2')
        self.Entry3 = interface.get_object('entry3')
        self.Entry4 = interface.get_object('entry4')
        self.Entry5 = interface.get_object('entry5')

        self.Button = interface.get_object('button1')

        interface.connect_signals(self)

    def on_window1_destroy(self, widget):
        global conn
        global cursor
        
        conn.commit()
        cursor.close
        Gtk.main_quit()

    def on_button1_clicked(self, widget):
        global cursor
        
        code = str(self.Entry1.get_text())
        statut = str(self.Entry2.get_text())
        nom = str(self.Entry3.get_text())
        prenom = str(self.Entry4.get_text())
        regime = str(self.Entry5.get_text())

        if code == '' or nom == '' or prenom == '' or statut == '':
            self.Label.set_text('Remplissez tous les champs (*)')

        else:
            try:
                cursor.execute("""INSERT INTO base VALUES(?,?,?,?,?)""",(code,statut,nom,prenom,regime))
                self.Label.set_text('Le code a été ajouté !')
                
            except sqlite3.OperationalError:
                print('Datab.db est probablement en cours d\'utilisation. Fermez l\'instance et réessayez !')
                
            except:
                self.Label.set_text('Une erreur est survenue !')

if __name__ == "__main__":
    ajoutCode()
    Gtk.main()
        


