import time, thread, serial, collections, grbl_tools
from serial.tools.list_ports_windows import *

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

class grbl_protocol():
    def __init__( self ):
        self.pile = collections.deque()
        self.liaison_active = False
        self.serie = comm()
        self.liste_attente = collections.deque()
        self.reponse = ( 'ok', 'error: Bad number format', 'error: Unsupported statement', "error: Invalid statement", 'error: Modal group violation', 'error: Expected command letter' )
        #self.status = ""
        self.pause = False
        self.streaming = False
        self.dispo = True

    def start_liaison( self , status ):
        self.liaison_active = True
        thread.start_new_thread( self.liaison_alle, () )
        thread.start_new_thread( self.liaison_retour, ( status, ) )

    def stop_liaison( self ):
        self.liaison_active = False
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
                    if self.dispo:
                        self.serie.envoyer( '?' )

    def liaison_retour( self, status ):
        while self.liaison_active == True:
            if self.serie.isOpen():
                temp = self.serie.recevoir()
                if temp.strip() in self.reponse and self.streaming:
                    tmp = self.liste_attente.popleft()
                    print tmp + " " + temp
                else:
                    if temp.strip() not in self.reponse:
                        #elf.status = temp
                        status.set( temp.strip() )
            else:
                time.sleep( 1 )

if __name__ == "__main__":
    list = grbl_tools.File_to_list()
    test = grbl_protocol()
    test.start_liaison()
    test.serie.set_port( 'com5' )
    test.add_commande( "G91\nG21\nG00 Y 1\n~\n~" )
    time.sleep( 5 )
    test.stop_liaison()
