'''
Created on 15 fevr. 2014

@author: guill

'''

import time, thread, serial, collections, grbl_tools
from serial.tools.list_ports_windows import *
from Tkinter import StringVar

class comm:
    def __init__( self ):
        self.DEFAULT_BAUDRATE = 9600
        self.Connec = serial.Serial()
        self.Connec.port = None
        self.Connec.baudrate = self.DEFAULT_BAUDRATE

    def scan( self ):
        available = []
        for port, desc, hwid in sorted( comports() ):
            if "USB" in desc:
                available.append( port )
        available.append( "Deconnexion" )
        return available

    def isOpen( self ):
       return self.Connec.isOpen()

    def set_port( self, port ):
        self.Connec.setPort( port )
        self.Connec.open()
        self.Connec.flushInput()
        if self.Connec.isOpen(): return True
        else: return False

    def get_connection( self ):
        return self.Connec

    def envoyer( self, message ):
        if self.Connec.isOpen():
            if self.Connec.writable():
                try:
                    self.Connec.write( message )
                except serial.SerialException, e:
                    pass

    def recevoir( self ):
        grbl_out = self.Connec.readline()
        return grbl_out

class status_coord:
    def __init__( self ):
        # mc = coordonnee de la machine
        # tc = coordonnee de travail
        self.mc_x = StringVar()
        self.mc_y = StringVar()
        self.mc_z = StringVar()
        self.tc_x = StringVar()
        self.tc_y = StringVar()
        self.tc_z = StringVar()
        self.status_travail = StringVar()


    def set( self, message ):
        temp = message.strip()[1:][:-1].split( ',' )
        self.mc_x.set( temp[1][5:] )
        self.mc_y.set( temp[2] )
        self.mc_z.set( temp[3] )
        self.tc_x.set( temp[4][5:] )
        self.tc_y.set( temp[5] )
        self.tc_z.set( temp[6] )
        self.status_travail.set( temp[0] )


class grbl_protocol():
    def __init__( self ):
        self.pile = collections.deque()
        self.grbl_stat_template = collections.namedtuple( 'grbl_stat', ['motion', 'activ_work_coord_sys', 'plan', 'metric', 'absolut', 'feedrate_mode', 'prrogram_flow', 'spindle_stat', 'coolant_stat', 'ntool', 'feedrate'] )
        self.grbl_stat = ""
        self.liaison_active = False
        self.serie = comm()
        self.liste_attente = collections.deque()
        self.reponse = ( 'ok', 'error: Bad number format', 'error: Unsupported statement', "error: Invalid statement", 'error: Modal group violation', 'error: Expected command letter' )
        self.reponse_event = {'ok' : self.liste_attente.popleft,
                              'error: Bad number format': self.liste_attente.popleft,
                              'error: Unsupported statement': self.liste_attente.popleft,
                              'error: Invalid statement': self.liste_attente.popleft,
                              'error: Modal group violation': self.liste_attente.popleft,
                              'error: Expected command letter': self.liste_attente.popleft,
                              'grbl_stat': self.status_commandes,
                              'grbl_coord': self.status_coord
                              }
        self.stat_coord = status_coord()
        #self.status = ""
        self.pause = False
        self.streaming = False

    def status_coord( self, coord ):
        pass

    def status_commandes( self, grbl_stat ):
        tmp = grbl_stat.strip()[1:][:-1].split( ' ' )
        self.grbl_stat = self.grbl_stat_template( *tmp )
        return self.grbl_stat.motion

    def start_liaison( self , affiche_texte ):
        self.liaison_active = True
        thread.start_new_thread( self.liaison_alle, () )
        thread.start_new_thread( self.liaison_retour, ( affiche_texte , ) )

    def stop_liaison( self ):
        self.liaison_active = False
        time.sleep( 0.2 )
        if self.serie.isOpen():
            self.serie.Connec.flushInput()
            self.serie.Connec.close()

    def add_commande( self, commande ):
        temp = filter( None, commande.split( "\n" ) )
        for i in temp:
            self.pile.append( i.strip() )

    def liaison_alle( self ):
        while self.liaison_active == True:
            commande_courante = ""
            if self.serie.isOpen():
                if self.pile.__len__() > 0 and self.liste_attente.__len__() < 5 and self.streaming:
                        commande_courante = self.pile.popleft()
                        self.serie.envoyer( commande_courante + '\n' )
                        self.liste_attente.append( commande_courante )
                else:
                    time.sleep( 0.3 )
                    self.serie.envoyer( '?' )
                    if self.streaming == False:
                        self.serie.envoyer( '$G\n' )

    def liaison_retour( self, affiche ):
        while self.liaison_active == True:
            if self.serie.isOpen():
                temp = self.serie.recevoir()
                if temp.strip() in self.reponse_event and self.streaming:
                    print temp.strip() + "\n"
                    tmp = self.reponse_event.get( temp.strip() )()
                    affiche( tmp + " " + temp )
                elif temp.strip().startswith( '[G' ):
                    self.reponse_event.get( 'grbl_stat' )( temp )
                elif temp.strip().startswith( '<' ):
                    self.reponse_event.get( 'grbl_coord' )( temp )
                    self.stat_coord.set( temp.strip() )


            else:
                time.sleep( 1 )

if __name__ == "__main__":
    list = grbl_tools.File_to_list()
    test = grbl_protocol()
    test.start_liaison()
    test.serie.set_port( 'com5' )
    time.sleep( 5 )
    test.stop_liaison()
